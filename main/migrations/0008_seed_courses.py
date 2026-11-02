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

# Shared with 0009 so the two cannot drift apart.
from ._course_seed_data import COURSES


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
