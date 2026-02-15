from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from .models import Post, Category, Tag, Comment

def post_list(request):
    """Display all published blog posts"""
    posts = Post.objects.filter(status='published')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Tag filter
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get sidebar data
    categories = Category.objects.annotate(post_count=Count('posts'))
    recent_posts = Post.objects.filter(status='published')[:5]
    tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'tags': tags,
        'search_query': search_query,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    """Display a single blog post with all media"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count
    post.increment_views()
    
    # Handle comment submission
    if request.method == 'POST':
        comment = Comment(
            post=post,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            website=request.POST.get('website', ''),
            comment=request.POST.get('comment')
        )
        comment.save()
        messages.success(request, 'Your comment has been submitted and awaits approval.')
        return redirect('blog:post_detail', slug=post.slug)
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True)
    
    # Get related posts (same category)
    related_posts = Post.objects.filter(
        category=post.category, 
        status='published'
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)

def category_list(request, slug):
    """Display posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'blog/category_list.html', context)

def tag_list(request, slug):
    """Display posts by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tag': tag,
    }
    return render(request, 'blog/tag_list.html', context)