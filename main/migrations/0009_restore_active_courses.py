"""Make sure the live site has course listings again.

0008 seeded the Course table, but only when the table was completely empty:

    if Course.objects.exists():
        return

On production that guard held — the courses page went live showing "Course
listings are being updated" and the navigation's course menu was empty, so
the table has rows but none of them active. Until this release the course
content was hardcoded in the template, so an empty table was invisible;
now that the page reads from the database it is the whole page.

This migration restores the listings without overwriting anything:

- If any active course exists, it does nothing at all. Someone is managing
  the table through the admin and this must not interfere.
- Otherwise, for each of the six courses it creates the row if the title is
  missing, or simply switches an existing row back on. Existing rows keep
  their own description, duration, pricing and image — only is_active
  changes.

It is deliberately irreversible in the data sense: reversing it does not
delete courses, because by then they may have been edited in the admin and
reversing a migration should not destroy someone's content. 0008 still
carries the matching unseed for a true teardown.
"""

from django.db import migrations

from ._course_seed_data import COURSES


def restore_active_courses(apps, schema_editor):
    Course = apps.get_model('main', 'Course')

    if Course.objects.filter(is_active=True).exists():
        # The site has course listings; nothing to repair.
        return

    for data in COURSES:
        course, created = Course.objects.get_or_create(
            title=data['title'],
            defaults={**data, 'is_active': True},
        )
        if not created and not course.is_active:
            # Keep whatever the row already says; just put it back on the site.
            course.is_active = True
            course.save(update_fields=['is_active'])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_seed_courses'),
    ]

    operations = [
        migrations.RunPython(restore_active_courses, migrations.RunPython.noop),
    ]
