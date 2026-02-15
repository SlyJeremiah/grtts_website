from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, PostImage, PostFile, PostVideo, Comment

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3
    fields = ['image', 'caption', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1
    fields = ['title', 'file', 'file_type', 'file_preview']
    readonly_fields = ['file_preview']
    
    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"
    file_preview.short_description = "File Link"

class PostVideoInline(admin.TabularInline):
    model = PostVideo
    extra = 1
    fields = ['title', 'video_url', 'description']

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ['name', 'email', 'comment', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Posts"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'published_date', 'views', 'media_count']
    list_filter = ['status', 'category', 'tags', 'published_date']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = ['views', 'featured_image_preview', 'media_count', 'published_date']
    inlines = [PostImageInline, PostVideoInline, PostFileInline, CommentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'tags', 'author')
        }),
        ('Featured Media', {
            'fields': ('featured_image', 'featured_image_preview', 'featured_video'),
            'classes': ('wide',)
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'published_date', 'views'),
            'classes': ('wide',)
        }),
    )
    
    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 100%;" />', obj.featured_image.url)
        return "No image"
    featured_image_preview.short_description = "Featured Image Preview"
    
    def media_count(self, obj):
        images = obj.images.count()
        videos = obj.videos.count()
        files = obj.files.count()
        return f"🖼️ {images} | 🎥 {videos} | 📎 {files}"
    media_count.short_description = "Media"

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'image_preview', 'caption', 'uploaded_at']
    list_filter = ['post']
    search_fields = ['post__title', 'caption']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(PostFile)
class PostFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'post', 'file_type', 'file_size_display', 'downloads']
    list_filter = ['file_type', 'post']
    search_fields = ['title', 'post__title']
    readonly_fields = ['downloads', 'file_link']
    
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download File</a>', obj.file.url)
        return "No file"
    file_link.short_description = "File Link"
    
    def file_size_display(self, obj):
        return obj.file_size()
    file_size_display.short_description = "File Size"

@admin.register(PostVideo)
class PostVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'post', 'video_preview']
    list_filter = ['post']
    search_fields = ['title', 'post__title']
    
    def video_preview(self, obj):
        if obj.video_url:
            return format_html('<a href="{}" target="_blank">Watch Video</a>', obj.video_url)
        return "No video"
    video_preview.short_description = "Video"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'comment_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'comment']
    list_editable = ['is_approved']
    readonly_fields = ['name', 'email', 'website', 'comment', 'created_at']
    
    def comment_preview(self, obj):
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = "Comment"
    
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"