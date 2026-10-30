from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Category, Post, Tag
from main.models import Course, DeploymentLocation


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    protocol = 'https'

    # Priority reflects how much each page matters to landowners, NGOs and
    # conservancies looking for ranger deployment and management contracts.
    pages = {
        'main:home': 1.0,
        'main:about': 0.9,
        'main:locations': 0.9,
        'main:contact': 0.8,
        'main:courses': 0.8,
        'main:apply_now': 0.7,
        'main:gis_applications': 0.6,
        'main:careers': 0.6,
        'main:faq': 0.5,
        'main:verify_certificate': 0.5,
        'blog:post_list': 0.6,
    }

    def items(self):
        return list(self.pages)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.pages[item]


class CourseSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Course.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('main:course_detail', args=[obj.id])


class LocationSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return DeploymentLocation.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('main:location_detail', args=[obj.id])


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4
    protocol = 'https'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('blog:category_list', args=[obj.slug])


class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.3
    protocol = 'https'

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return reverse('blog:tag_list', args=[obj.slug])


SITEMAPS = {
    'static': StaticViewSitemap,
    'courses': CourseSitemap,
    'locations': LocationSitemap,
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
}
