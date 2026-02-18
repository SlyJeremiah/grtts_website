from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Main blog listing
    path('', views.post_list, name='post_list'),
    
    # Post detail
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    
    # Category and tag listings
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('tag/<slug:slug>/', views.tag_list, name='tag_list'),
]
