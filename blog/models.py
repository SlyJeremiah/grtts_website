from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import os

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
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    # Fixed: Use string reference with correct case
    author = models.ForeignKey('main.User', on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    
    # Content
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True, null=True)
    featured_video = models.URLField(blank=True, null=True, help_text="YouTube or Vimeo video URL")
    excerpt = models.TextField(max_length=300, help_text="Short summary of the post")
    content = models.TextField(help_text="Main content of the post")
    
    # Metadata
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def increment_views(self):
        self.views += 1
        self.save()

class PostImage(models.Model):
    """Additional images for blog posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog/images/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Image for {self.post.title}"

class PostFile(models.Model):
    """File attachments for blog posts (PDFs, documents, etc.)"""
    FILE_TYPES = [
        ('pdf', 'PDF Document'),
        ('doc', 'Word Document'),
        ('xls', 'Excel Spreadsheet'),
        ('ppt', 'PowerPoint Presentation'),
        ('txt', 'Text File'),
        ('other', 'Other'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='blog/files/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='other')
    title = models.CharField(max_length=200, help_text="Display name for the file")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    downloads = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} for {self.post.title}"
    
    def filename(self):
        return os.path.basename(self.file.name)
    
    def file_size(self):
        if self.file:
            try:
                size = self.file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size/1024:.1f} KB"
                else:
                    return f"{size/(1024*1024):.1f} MB"
            except:
                return "Unknown"
        return "No file"

class PostVideo(models.Model):
    """Embedded videos for blog posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    video_url = models.URLField(help_text="YouTube or Vimeo video URL")
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Video for {self.post.title}"

class Comment(models.Model):
    """Comments on blog posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"