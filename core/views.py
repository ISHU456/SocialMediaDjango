from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post


def landing_page(request):
    """Landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('posts:home')
    
    # Get some sample posts for demonstration
    sample_posts = Post.objects.filter(is_public=True).select_related('user', 'user__profile')[:3]
    
    context = {
        'sample_posts': sample_posts,
    }
    return render(request, 'core/landing.html', context)


@login_required
def dashboard(request):
    """Dashboard view for authenticated users"""
    return redirect('posts:home')
