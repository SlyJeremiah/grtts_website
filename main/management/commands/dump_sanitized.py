"""Export the database with personal data and secrets scrubbed.

Produces a Django fixture that can be loaded into a local database with
`loaddata`, so development work runs against realistic content and realistic
row counts without handling anyone's real personal information.

    python manage.py dump_sanitized --output grtts-sanitized.json

Why a fixture rather than pg_dump: it needs no PostgreSQL client tools (whose
major version must match the server), it is plain JSON you can inspect before
sending, and the schema comes from migrations anyway.

Scrubbing is allow-list driven: SCRUB below names every field to replace, and
anything not listed is exported as-is. Run with --audit to list text fields on
sensitive models that are NOT being scrubbed, so new fields cannot silently
start leaking.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from django.apps import apps
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.db import models

# Models whose rows are personal data or credentials. Field -> replacement
# strategy. Strategies: 'name', 'email', 'phone', 'text', 'blank', 'secret',
# 'ip', 'id_number', 'password', 'json', 'username', and 'keep'.
#
# 'keep' means the field was reviewed and deliberately exported unchanged.
# Every text field on a model listed here must have a rule, so a newly added
# field fails the --audit check rather than silently leaking.
SCRUB: dict[str, dict[str, str]] = {
    'main.User': {
        'first_name': 'name', 'last_name': 'name', 'email': 'email',
        'phone': 'phone', 'id_number': 'id_number', 'password': 'password',
        'email_verification_token': 'blank', 'reset_token': 'blank',
        'username': 'username',
    },
    'main.ApplicantProfile': {
        'address': 'text', 'city': 'text', 'emergency_name': 'name',
        'emergency_phone': 'phone', 'emergency_relationship': 'text',
        'medical_conditions': 'text', 'dietary_requirements': 'text',
        'nationality': 'keep', 'province': 'keep',
    },
    'main.CourseApplication': {
        'motivation_text': 'text', 'previous_experience': 'text',
        'medical_conditions': 'text', 'dietary_requirements': 'text',
        'interview_notes': 'text', 'admin_notes': 'text',
        'application_number': 'keep',
    },
    'main.CourseRegistration': {
        'full_name': 'name', 'id_number': 'id_number', 'email': 'email',
        'phone': 'phone', 'alternate_phone': 'phone', 'address': 'text',
        'emergency_name': 'name', 'emergency_phone': 'phone',
        'emergency_relationship': 'text', 'medical_conditions': 'text',
        'dietary_requirements': 'text', 'admin_notes': 'text',
        'registration_number': 'keep', 'accommodation_dates': 'keep',
    },
    'main.JobApplication': {
        'first_name': 'name', 'last_name': 'name', 'email': 'email',
        'phone': 'phone', 'cover_letter': 'text', 'current_employer': 'text',
        'current_position': 'text', 'notes': 'text', 'ip_address': 'ip',
        'user_agent': 'blank',
    },
    'main.Donation': {
        'donor_name': 'name', 'donor_email': 'email', 'donor_phone': 'phone',
        'payment_reference': 'blank', 'payment_response': 'json',
        'transaction_id': 'keep',
    },
    'main.Payment': {
        'mobile_number': 'phone', 'provider_reference': 'blank',
        'request_data': 'json', 'response_data': 'json',
        'card_last4': 'blank',   # cardholder data — never leaves production
        'card_brand': 'keep',
    },
    'main.PaymentWebhook': {
        'payload': 'json', 'provider': 'keep', 'event_type': 'keep',
    },
    'main.PaymentMethod': {
        # Live gateway credentials live in this table.
        'api_key': 'secret', 'api_secret': 'secret', 'merchant_number': 'phone',
        'display_name': 'keep', 'instructions': 'keep',
    },
    'main.NewsletterSubscriber': {
        'email': 'email', 'first_name': 'name', 'last_name': 'name',
        'ip_address': 'ip', 'source': 'keep',
    },
    'main.ContactMessage': {
        'name': 'name', 'email': 'email', 'phone': 'phone', 'message': 'text',
        'subject': 'text',
    },
    'main.StudentInquiry': {
        'name': 'name', 'email': 'email', 'phone': 'phone',
        'experience': 'text',
        'nationality': 'keep', 'education': 'keep', 'intake': 'keep',
    },
    'main.LandownerInquiry': {
        'name': 'name', 'email': 'email', 'phone': 'phone',
        'organization': 'text', 'property_location': 'text', 'details': 'text',
    },
    'main.EnthusiastInquiry': {
        'name': 'name', 'email': 'email', 'background': 'text',
        'message': 'text', 'availability': 'keep',
    },
    'main.OtherInquiry': {
        'name': 'name', 'email': 'email', 'phone': 'phone',
        'organization': 'text', 'subject': 'text', 'message': 'text',
    },
    'main.Certificate': {
        'full_name': 'name',
        # Kept so certificate verification can be exercised locally; they
        # identify a certificate, not a person, and the name is scrubbed.
        'certificate_number': 'keep', 'verification_token': 'keep',
        'course_name': 'keep', 'grade': 'keep', 'duration': 'keep',
    },
    'main.CertificateVerificationLog': {'ip_address': 'ip', 'user_agent': 'blank'},
    'main.UserDocument': {'description': 'text'},
    'blog.Comment': {
        'name': 'name', 'email': 'email', 'website': 'blank',
        'content': 'text', 'ip_address': 'ip',
    },
}

# Never exported. Content types and permissions are recreated by migrate;
# exporting them makes the fixture collide with a freshly migrated database.
EXCLUDE_MODELS = {
    'sessions.Session', 'admin.LogEntry',
    'contenttypes.ContentType', 'auth.Permission',
}

FIRST_NAMES = ['Tendai', 'Rudo', 'Farai', 'Chipo', 'Tatenda', 'Nyasha',
               'Kudzai', 'Rutendo', 'Tafara', 'Anesu']
LAST_NAMES = ['Moyo', 'Ncube', 'Dube', 'Sibanda', 'Chirwa', 'Mhlanga',
              'Banda', 'Phiri', 'Mutasa', 'Zhou']


def _seed(model_label: str, pk, field: str) -> int:
    """Stable pseudo-random seed, so repeated dumps produce the same values."""
    digest = hashlib.sha256(f'{model_label}:{pk}:{field}'.encode()).hexdigest()
    return int(digest[:8], 16)


def fake(strategy: str, model_label: str, pk, field: str, original):
    n = _seed(model_label, pk, field)

    if strategy == 'keep':
        return original
    if strategy == 'password':
        return '!scrubbed-unusable-password'
    if strategy == 'blank':
        return '' if isinstance(original, str) else None
    if strategy == 'secret':
        return '' if original else original
    if strategy == 'json':
        return None if original is not None else original
    if strategy == 'ip':
        return f'198.51.100.{n % 254 + 1}' if original else original

    if original in (None, ''):
        return original

    if strategy == 'name':
        return f'{FIRST_NAMES[n % len(FIRST_NAMES)]} {LAST_NAMES[(n // 7) % len(LAST_NAMES)]}'
    if strategy == 'email':
        return f'redacted{n % 10000}@example.invalid'
    if strategy == 'phone':
        return f'+26377{n % 10000000:07d}'
    if strategy == 'username':
        return f'user{n % 100000}'
    if strategy == 'id_number':
        return f'00-{n % 1000000:06d}X00'
    if strategy == 'text':
        words = len(str(original).split())
        return f'[redacted: {words} word(s) of original content]'
    return original


class Command(BaseCommand):
    help = 'Export all data with personal information and secrets scrubbed.'

    def add_arguments(self, parser):
        parser.add_argument('--output', default='grtts-sanitized.json',
                            help='Destination file (default: grtts-sanitized.json)')
        parser.add_argument('--audit', action='store_true',
                            help='List unscrubbed text fields on sensitive models and exit.')
        parser.add_argument('--indent', type=int, default=2)

    def handle(self, *args, **options):
        if options['audit']:
            return self.audit()

        output = Path(options['output'])
        objects = []
        counts: dict[str, int] = {}
        scrubbed_fields = 0

        for model in apps.get_models():
            label = f'{model._meta.app_label}.{model.__name__}'
            if label in EXCLUDE_MODELS:
                continue

            rules = SCRUB.get(label, {})
            rows = list(model._default_manager.all())
            if not rows:
                continue
            counts[label] = len(rows)

            for obj in rows:
                for field_name, strategy in rules.items():
                    if not hasattr(obj, field_name):
                        continue
                    current = getattr(obj, field_name)
                    replacement = fake(strategy, label, obj.pk, field_name, current)
                    if replacement != current:
                        scrubbed_fields += 1
                    setattr(obj, field_name, replacement)
                objects.append(obj)

        data = serializers.serialize('json', objects, indent=options['indent'])
        output.write_text(data, encoding='utf-8')

        self.stdout.write('')
        for label in sorted(counts):
            marker = 'scrubbed' if label in SCRUB else ''
            self.stdout.write(f'  {label:42} {counts[label]:>6}  {marker}')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Wrote {output} — {len(objects)} rows, '
            f'{scrubbed_fields} field values scrubbed, '
            f'{output.stat().st_size / 1024:.1f} KB'
        ))
        self.stdout.write(
            'Review the file before sending it. Load it with:\n'
            '    python manage.py loaddata ' + str(output)
        )

    def audit(self):
        """Flag text fields on sensitive models that no rule covers."""
        problems = 0
        for label, rules in SCRUB.items():
            app_label, model_name = label.split('.')
            try:
                model = apps.get_model(app_label, model_name)
            except LookupError:
                self.stderr.write(self.style.WARNING(f'{label}: model no longer exists'))
                continue
            for field in model._meta.get_fields():
                if not isinstance(field, (models.CharField, models.TextField,
                                          models.EmailField, models.JSONField,
                                          models.GenericIPAddressField)):
                    continue
                if field.name in rules or getattr(field, 'choices', None):
                    continue
                self.stdout.write(f'  {label}.{field.name} ({field.__class__.__name__}) not scrubbed')
                problems += 1
        if problems:
            raise CommandError(
                f'{problems} unscrubbed field(s) on sensitive models. '
                'Add a rule to SCRUB, or confirm the field holds no personal data.'
            )
        self.stdout.write(self.style.SUCCESS('All text fields on sensitive models are covered.'))
