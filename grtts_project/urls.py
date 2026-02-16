from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth import views as auth_views

# Simple ping view for testing
def ping(request):
    return HttpResponse("✅ Django is working on Vercel!")

urlpatterns = [
    # Health check endpoint
    path('ping/', ping, name='ping'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Main app URLs (home, courses, locations, etc.) - CORRECT
    path('', include('main.urls')),
    
    # Blog app URLs
    path('blog/', include('blog.urls')),
    
    # =========================================================================
    # AUTHENTICATION URLS
    # =========================================================================
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='main/login.html',
             redirect_authenticated_user=True
         ), 
         name='login'),
    
    path('logout/', 
         auth_views.LogoutView.as_view(
             next_page='home'
         ), 
         name='logout'),
    
    # Password Reset (optional - remove if you don't have templates yet)
    # path('password-reset/', 
    #      auth_views.PasswordResetView.as_view(
    #          template_name='main/password_reset.html',
    #      ), 
    #      name='password_reset'),
]

# =============================================================================
# SERVE MEDIA AND STATIC FILES IN DEVELOPMENT
# =============================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
