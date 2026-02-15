"""
Blog URL Configuration
"""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog post list (main blog page)
    path('', views.post_list, name='post_list'),
    
    # Individual blog post detail
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    
    # Posts by category
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    
    # Posts by tag
    path('tag/<slug:slug>/', views.tag_list, name='tag_list'),
    
    # IMPORTANT: No test-email URL here - that belongs in main app
]