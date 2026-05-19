from django.urls import path
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('contact/', views.contact, name='contact'),
    # add other URLs as needed
]