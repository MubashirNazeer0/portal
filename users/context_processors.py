from .models import Profile

def pending_users(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return {'pending_profiles': Profile.objects.filter(status='pending')}
    return {}
