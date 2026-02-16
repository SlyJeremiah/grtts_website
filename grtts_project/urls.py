from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def ping(request):
    return HttpResponse("✅ Django is working on Vercel!")

urlpatterns = [
    path('ping/', ping, name='ping'),
    path('admin/', admin.site.urls),  # Admin panel (for you only)
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
