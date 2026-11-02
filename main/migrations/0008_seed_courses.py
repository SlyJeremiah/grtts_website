"""Seed the Course table from the content previously hardcoded in templates.

The Course model, its admin and the courses view all existed, but the table
was empty in production and main/templates/main/courses.html carried the
course content as literal HTML. The view's filtering and search therefore ran
against an empty queryset and had no effect on what visitors saw, and GRTTS
could not change their own course listings without a developer.

This migration moves that exact content into the database. It is additive and
idempotent: it does nothing if any Course rows already exist, so it cannot
overwrite anything entered through the admin.

The three specialist courses were a single bulleted card in the template. They
are seeded as separate rows so each can be priced, scheduled, described and
retired independently.
"""

from django.db import migrations

COURSES = [
    {
        'title': 'Basic Ranger Course',
        'course_type': 'BASIC',
        'duration': '6 Weeks',
        'intake_dates': 'January, June, October',
        'description': (
            'Conservation Guardianship.\n\n'
            'Detailed entry level studies for individuals aspiring to join the '
            'field of wildlife protection and anti-poaching operations.'
        ),
    },
    {
        'title': 'Advanced Ranger & Patrol',
        'course_type': 'ADVANCED',
        'duration': '2 Weeks',
        'intake_dates': 'March, November',
        'description': 'Designed for rangers moving into leadership roles.',
    },
    {
        'title': 'Basic Tracking Course',
        'course_type': 'TRACKING',
        'duration': '7 Days',
        'intake_dates': 'Available on request',
        'description': (
            'Held at Victoria Falls, in a Big 5 area.\n\n'
            'The course covers:\n'
            '- Signs of the wild\n'
            '- The art of human and wildlife tracking\n'
            '- Tracking as a science\n'
            '- Track and sign identification\n'
            '- Trailing\n'
            '- Tracking evaluation\n\n'
            'Accommodation: tents are provided. Participants bring their own '
            'personal gear.'
        ),
    },
    {
        'title': 'Tracking: Basic, Advanced & Counter-Insurgency',
        'course_type': 'SPECIALIST',
        'duration': 'Varies by level',
        'intake_dates': 'Available all year round',
        'description': (
            'Specialist tracking instruction across basic, advanced and '
            'counter-insurgency disciplines.'
        ),
    },
    {
        'title': 'Small Team Tactics',
        'course_type': 'SPECIALIST',
        'duration': 'Varies by requirement',
        'intake_dates': 'Available all year round',
        'description': (
            'Specialist training in small team movement, formations and '
            'field tactics for anti-poaching units.'
        ),
    },
    {
        'title': 'K9 Handling & Kennel Management',
        'course_type': 'SPECIALIST',
        'duration': 'Varies by requirement',
        'intake_dates': 'Available all year round',
        'description': (
            'Specialist training in the handling, deployment and kennel '
            'management of anti-poaching working dogs.'
        ),
    },
]


def seed_courses(apps, schema_editor):
    Course = apps.get_model('main', 'Course')
    if Course.objects.exists():
        # Something is already managing this table; leave it alone.
        return
    Course.objects.bulk_create([
        Course(is_active=True, **data) for data in COURSES
    ])


def unseed_courses(apps, schema_editor):
    Course = apps.get_model('main', 'Course')
    Course.objects.filter(title__in=[c['title'] for c in COURSES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_partner'),
    ]

    operations = [
        migrations.RunPython(seed_courses, unseed_courses),
    ]
