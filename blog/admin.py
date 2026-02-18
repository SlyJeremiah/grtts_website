from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, PostImage, PostFile, PostVideo, Comment

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1
    fields = ['file', 'file_type', 'title', 'description']


class PostVideoInline(admin.TabularInline):
    model = PostVideo
    extra = 1
    fields = ['video', 'title', 'description', 'order', 'video_preview']
    readonly_fields = ['video_preview']
    
    def video_preview(self, obj):
        if obj.video:
            return format_html('<video width="100" height="60" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
        return "No video"
    video_preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'views', 'published_date', 'thumbnail_preview']
    list_filter = ['status', 'category', 'tags', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published_date'
    
    inlines = [PostImageInline, PostFileInline, PostVideoInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'tags', 'author')
        }),
        ('Main Content', {
            'fields': ('featured_image', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_video',),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Dates', {
            'fields': ('status', 'views', 'published_date'),
            'classes': ('wide',)
        }),
    )
    
    def thumbnail_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 5px;" />', obj.featured_image.url)
        return "No image"
    thumbnail_preview.short_description = "Thumbnail"
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'image_preview', 'caption', 'order', 'uploaded_at']
    list_filter = ['post', 'uploaded_at']
    search_fields = ['post__title', 'caption']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(PostFile)
class PostFileAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'file_type', 'file_link', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['post__title', 'title', 'description']
    
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        return "No file"
    file_link.short_description = "File"


@admin.register(PostVideo)
class PostVideoAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'order', 'video_preview', 'uploaded_at']
    list_filter = ['post', 'uploaded_at']
    search_fields = ['post__title', 'title', 'description']
    
    def video_preview(self, obj):
        if obj.video:
            return format_html('<video width="100" height="60" controls><source src="{}" type="video/mp4">Preview</video>', obj.video.url)
        return "No video"
    video_preview.short_description = "Preview"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"
