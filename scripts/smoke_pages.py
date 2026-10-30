"""Request every public route and report the status code.

A page that only breaks at render time (a bad {% url %}, a missing template)
returns 200 in no test at all, so this walks the real URL conf through the
Django test client and fails loudly on anything 4xx or 5xx.

Run with:
    DATABASE_URL="sqlite:///dev.sqlite3" DEBUG=True python scripts/smoke_pages.py
"""
import os
import sys
from pathlib import Path

# Run from anywhere: the project root is this file's parent's parent.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import django  # noqa: E402

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grtts_project.settings')
os.environ.setdefault('DEBUG', 'True')
django.setup()

from django.test.utils import setup_test_environment  # noqa: E402

setup_test_environment()

from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402

from main.models import Certificate, Course, DeploymentLocation, JobPost  # noqa: E402
from blog.models import Category, Post, Tag  # noqa: E402

# Routes that need no arguments.
SIMPLE_ROUTES = [
    'main:home',
    'main:about',
    'main:faq',
    'main:courses',
    'main:locations',
    'main:contact',
    'main:inquiry_page',
    'main:verify_certificate',
    'main:gis_applications',
    'main:apply_now',
    'main:careers',
    'main:register',
    'blog:post_list',
]

# Staff-only routes: a redirect to the admin login is the correct answer here.
STAFF_ROUTES = [
    'main:test_email',
    'main:debug_media',
    'main:newsletter_test_page',
    'main:newsletter_test',
]


def build_targets():
    targets = [(name, reverse(name)) for name in SIMPLE_ROUTES]

    contact = reverse('main:contact')
    courses = reverse('main:courses')
    locations = reverse('main:locations')
    targets += [
        ('contact ?type=student', contact + '?type=student'),
        ('contact ?type=enthusiast', contact + '?type=enthusiast'),
        ('contact ?type=other', contact + '?type=other'),
        ('contact ?type=general (legacy alias)', contact + '?type=general'),
        ('contact ?type=nonsense', contact + '?type=nonsense'),
        ('courses ?type=basic', courses + '?type=basic'),
        ('courses ?q=tracking', courses + '?q=tracking'),
        ('courses ?type=nonsense', courses + '?type=nonsense'),
        ('locations ?center=hwange', locations + '?center=hwange'),
        ('blog ?q=ranger', reverse('blog:post_list') + '?q=ranger'),
    ]

    course = Course.objects.first()
    if course:
        targets.append(('main:course_detail',
                        reverse('main:course_detail', args=[course.id])))
        targets.append(('contact ?course=<pk>',
                        contact + f'?type=student&course={course.id}'))

    location = DeploymentLocation.objects.first()
    if location:
        targets.append(('main:location_detail',
                        reverse('main:location_detail', args=[location.id])))

    job = JobPost.objects.filter(is_active=True).first()
    if job:
        targets.append(('main:job_apply', reverse('main:job_apply', args=[job.id])))

    cert = Certificate.objects.filter(is_valid=True).first()
    if cert:
        targets.append(('main:certificate_detail',
                        reverse('main:certificate_detail',
                                args=[cert.certificate_number])))

    targets.append(('main:unsubscribe_newsletter (unknown address)',
                    reverse('main:unsubscribe_newsletter',
                            args=['nobody@example.com'])))

    post = Post.objects.filter(status='published').first()
    if post:
        targets.append(('blog:post_detail',
                        reverse('blog:post_detail', args=[post.slug])))
    category = Category.objects.first()
    if category:
        targets.append(('blog:category_list',
                        reverse('blog:category_list', args=[category.slug])))
    tag = Tag.objects.first()
    if tag:
        targets.append(('blog:tag_list', reverse('blog:tag_list', args=[tag.slug])))

    targets.append(('sitemap.xml', '/sitemap.xml'))
    targets.append(('robots.txt', '/robots.txt'))
    targets += [(name + ' (staff only)', reverse(name)) for name in STAFF_ROUTES]

    return targets


def main():
    client = Client()
    failures = []
    skipped = []

    print(f"{'status':>6}  {'bytes':>7}  route")
    print('-' * 86)

    for name, url in build_targets():
        try:
            response = client.get(url)
        except Exception as exc:  # noqa: BLE001 — report, do not stop
            print(f"{'ERR':>6}  {'-':>7}  {name}  ->  {url}")
            failures.append((name, url, f'{type(exc).__name__}: {exc}'))
            continue

        size = len(response.content) if hasattr(response, 'content') else 0
        print(f'{response.status_code:>6}  {size:>7}  {name}  ->  {url}')
        if response.status_code >= 400:
            failures.append((name, url, f'HTTP {response.status_code}'))
        elif response.status_code == 200 and size < 1500 and 'staff only' not in name:
            # A real page on this layout is never this small.
            skipped.append((name, url, f'suspiciously small: {size} bytes'))

    print('-' * 86)

    for name, url, detail in skipped:
        print(f'NOTE  {name} ({url}): {detail}')

    if failures:
        print(f'\n{len(failures)} failure(s):')
        for name, url, detail in failures:
            print(f'  {name} ({url}): {detail}')
        sys.exit(1)

    print('\nEvery route returned a non-error status.')


if __name__ == '__main__':
    main()
