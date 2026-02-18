from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os

User = get_user_model()

class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Blog post tags"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Blog post model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', null=True, blank=True)
    
    # Main content
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="Short summary of the post")
    
    # Featured image
    featured_image = models.ImageField(
        upload_to='blog/featured/%Y/%m/',
        blank=True,
        null=True,
        help_text="Main featured image for the post"
    )
    
    # Meta fields
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title")
    meta_description = models.TextField(blank=True, help_text="SEO description")
    
    # Featured video (optional)
    featured_video = models.URLField(blank=True, help_text="YouTube or Vimeo URL")
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views = models.IntegerField(default=0)
    
    # Dates
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.content:
            # Auto-generate excerpt from content if not provided
            self.excerpt = self.content[:200] + '...'
        super().save(*args, **kwargs)


def post_image_upload_path(instance, filename):
    """Generate upload path for post images: blog/post_<id>/images/<filename>"""
    return f'blog/post_{instance.post.id}/images/{filename}'


class PostImage(models.Model):
    """Additional images for a blog post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=post_image_upload_path)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"Image for {self.post.title}"

    def filename(self):
        return os.path.basename(self.image.name)


def post_file_upload_path(instance, filename):
    """Generate upload path for post files: blog/post_<id>/files/<filename>"""
    return f'blog/post_{instance.post.id}/files/{filename}'


class PostFile(models.Model):
    """File attachments for a blog post"""
    FILE_TYPES = [
        ('pdf', 'PDF Document'),
        ('doc', 'Word Document'),
        ('xls', 'Excel Spreadsheet'),
        ('ppt', 'PowerPoint Presentation'),
        ('other', 'Other'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=post_file_upload_path)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default='other')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"File for {self.post.title}"

    def filename(self):
        return os.path.basename(self.file.name)


def post_video_upload_path(instance, filename):
    """Generate upload path for post videos: blog/post_<id>/videos/<filename>"""
    return f'blog/post_{instance.post.id}/videos/{filename}'


class PostVideo(models.Model):
    """Video uploads for a blog post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to=post_video_upload_path)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"Video for {self.post.title}"


class Comment(models.Model):
    """Blog post comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, help_text="Optional website URL")
    content = models.TextField()
    
    approved = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
