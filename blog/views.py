from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from .models import Post, Category, Tag, Comment

def post_list(request):
    """Display all published blog posts"""
    posts = Post.objects.filter(status='published').order_by('-published_date')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
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
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:10]
    
    recent_posts = Post.objects.filter(
        status='published'
    ).order_by('-published_date')[:5]
    
    tags = Tag.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:20]
    
    context = {
        'page_obj': page_obj,
        'search_query': query,
        'categories': categories,
        'recent_posts': recent_posts,
        'tags': tags,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Display a single blog post"""
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts (same category)
    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id).distinct()[:3]
    
    # Get approved comments
    comments = post.comments.filter(approved=True).order_by('-created_at')
    
    # Handle comment submission
    if request.method == 'POST' and request.POST.get('comment'):
        comment = Comment(
            post=post,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            content=request.POST.get('comment'),
            ip_address=request.META.get('REMOTE_ADDR')
        )
        comment.save()
        messages.success(request, 'Your comment has been submitted and is awaiting approval.')
        return redirect('blog:post_detail', slug=post.slug)
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)


def category_list(request, slug):
    """Display posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        category=category, 
        status='published'
    ).order_by('-published_date')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'post_count': posts.count(),
    }
    return render(request, 'blog/category_list.html', context)


def tag_list(request, slug):
    """Display posts by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(
        tags=tag, 
        status='published'
    ).order_by('-published_date')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'post_count': posts.count(),
    }
    return render(request, 'blog/tag_list.html', context)
