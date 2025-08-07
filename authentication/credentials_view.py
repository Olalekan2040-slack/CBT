from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def credentials_view(request):
    """Display system credentials for testing"""
    
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'authentication/credentials.html', context)
