from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from .models import Post, Category, Tag, Comment

def post_list(request):
    posts = Post.objects.filter(status='published')
    
    # Search
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(categories__slug=category_slug)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = Category.objects.annotate(post_count=Count('posts'))
    recent_posts = Post.objects.filter(status='published')[:3]
    tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
        'tags': tags,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    post.views += 1
    post.save()
    
    # Get related posts
    related_posts = Post.objects.filter(
        categories__in=post.categories.all()
    ).exclude(id=post.id).distinct()[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_list.html', context)


def tag_list(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_list.html', context)
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
