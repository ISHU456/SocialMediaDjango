from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from posts.models import Post, Notification


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    
    # Get user's posts
    posts = Post.objects.filter(user=user, is_public=True).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check if current user is following this profile
    is_following = request.user.profile.following.filter(id=profile.id).exists()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'page_obj': page_obj,
        'is_following': is_following,
        'posts_count': posts.count(),
    }
    return render(request, 'profiles/profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:profile_view', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profiles/profile_edit.html', context)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        messages.error(request, 'You cannot follow yourself!')
        return redirect('profiles:profile_view', username=username)
    
    profile_to_follow = user_to_follow.profile
    current_user_profile = request.user.profile
    
    if current_user_profile.following.filter(id=profile_to_follow.id).exists():
        # Unfollow
        current_user_profile.following.remove(profile_to_follow)
        messages.success(request, f'You unfollowed {user_to_follow.username}')
    else:
        # Follow
        current_user_profile.following.add(profile_to_follow)
        messages.success(request, f'You are now following {user_to_follow.username}')
        
        # Create notification
        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            notification_type='follow'
        )
    
    return redirect('profiles:profile_view', username=username)


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.profile.followers.all()
    
    paginator = Paginator(followers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': user,
        'page_obj': page_obj,
        'list_type': 'followers',
    }
    return render(request, 'profiles/followers_following.html', context)


@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = user.profile.following.all()
    
    paginator = Paginator(following, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': user,
        'page_obj': page_obj,
        'list_type': 'following',
    }
    return render(request, 'profiles/followers_following.html', context)


@login_required
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=request.user.id)
    else:
        users = User.objects.none()
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'profiles/search_users.html', context)


@login_required
def suggested_users(request):
    # Get users that the current user is not following
    following_profiles = request.user.profile.following.all()
    following_users = User.objects.filter(profile__in=following_profiles)
    suggested_users = User.objects.exclude(
        id__in=[user.id for user in following_users] + [request.user.id]
    )[:10]
    
    context = {
        'suggested_users': suggested_users,
    }
    return render(request, 'profiles/suggested_users.html', context)
