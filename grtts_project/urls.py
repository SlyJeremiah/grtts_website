from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth import views as auth_views

def ping(request):
    return HttpResponse("✅ Django is working on Vercel!")

urlpatterns = [
    path('ping/', ping, name='ping'),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
    
    # Logout URL - Fixed
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
