from .models import Partner

def partners(request):
    return {
        'partners': Partner.objects.filter(is_active=True).order_by('order', 'name')
    }