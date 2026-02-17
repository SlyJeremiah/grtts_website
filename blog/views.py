from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from .models import Post, Category, Tag, Comment

def post_list(request):
    # Get all published posts
    posts = Post.objects.filter(status='published').select_related('author').prefetch_related('categories', 'tags')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Get filter parameters
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    
    if category_slug:
        posts = posts.filter(categories__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Pagination
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get sidebar data
    categories = Category.objects.annotate(post_count=models.Count('posts'))
    recent_posts = Post.objects.filter(status='published').order_by('-published_date')[:5]
    tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'categories': categories,
        'recent_posts': recent_posts,
        'tags': tags,
    }
    return render(request, 'blog/post_list.html', context)

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
