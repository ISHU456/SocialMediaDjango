from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.models import User
from .models import Post, Comment, Share, Notification, Hashtag
from .forms import PostForm, CommentForm, ShareForm
from profiles.models import Profile


@login_required
def home(request):
    """Display home feed with posts from followed users and public posts"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('posts:home')
    else:
        form = PostForm()
    
    # Get posts from followed users and public posts
    followed_users = [profile.user for profile in request.user.profile.followers.all()]
    followed_users.append(request.user)  # Include own posts
    
    posts = Post.objects.filter(
        Q(user__in=followed_users) | Q(is_public=True)
    ).select_related('user', 'user__profile').prefetch_related('hashtags', 'likes', 'comments').distinct()
    
    # Get trending hashtags
    trending_hashtags = Hashtag.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0).order_by('-post_count')[:10]
    
    # Get suggested users (users not being followed)
    following_users = [profile.user for profile in request.user.profile.following.all()]
    suggested_users = User.objects.exclude(
        id__in=[request.user.id] + [user.id for user in following_users]
    ).select_related('profile')[:10]
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'post_form': form,
        'trending_hashtags': trending_hashtags,
        'suggested_users': suggested_users,
    }
    return render(request, 'posts/home.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('posts:home')
    else:
        form = PostForm()
    
    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user can view this post
    if not post.can_user_view(request.user):
        messages.error(request, "You don't have permission to view this post.")
        return redirect('posts:home')
    
    comments = post.comments.filter(parent=None).select_related('user', 'user__profile')
    comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/post_form.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('posts:home')
    
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


@login_required
def like_post(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        
        # Check if user can interact with this post
        if not post.can_user_interact(request.user):
            return JsonResponse({
                'error': 'You don\'t have permission to like this post.'
            }, status=403)
        
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
            # Create notification
            if request.user != post.user:
                Notification.objects.create(
                    recipient=post.user,
                    sender=request.user,
                    notification_type='like',
                    post=post
                )
        
        # Always return JSON response for AJAX requests
        return JsonResponse({
            'liked': liked,
            'likes_count': post.get_likes_count()
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
def like_comment(request, pk):
    try:
        comment = get_object_or_404(Comment, pk=pk)
        
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True
            # Create notification
            if request.user != comment.user:
                Notification.objects.create(
                    recipient=comment.user,
                    sender=request.user,
                    notification_type='like',
                    comment=comment
                )
        
        # Always return JSON response for AJAX requests
        return JsonResponse({
            'liked': liked,
            'likes_count': comment.get_likes_count()
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user can interact with this post
    if not post.can_user_interact(request.user):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'You don\'t have permission to comment on this post.'
            }, status=403)
        else:
            messages.error(request, "You don't have permission to comment on this post.")
            return redirect('posts:home')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            
            # Create notification
            if request.user != post.user:
                Notification.objects.create(
                    recipient=post.user,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.pk,
                    'message': 'Comment added successfully!'
                })
            else:
                messages.success(request, 'Comment added successfully!')
                return redirect('posts:post_detail', pk=pk)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    
    return redirect('posts:post_detail', pk=pk)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    post_pk = comment.post.pk
    comment.delete()
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Comment deleted successfully!'
        })
    else:
        messages.success(request, 'Comment deleted successfully!')
        return redirect('posts:post_detail', pk=post_pk)


@login_required
def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user can view this post
    if not post.can_user_view(request.user):
        messages.error(request, "You don't have permission to view this post.")
        return redirect('posts:home')
    
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            share = form.save(commit=False)
            share.post = post
            share.user = request.user
            share.save()
            
            # Create notification
            if request.user != post.user:
                Notification.objects.create(
                    recipient=post.user,
                    sender=request.user,
                    notification_type='share',
                    post=post
                )
            
            messages.success(request, 'Post shared successfully!')
            return redirect('posts:home')
    else:
        form = ShareForm()
    
    return render(request, 'posts/share_post.html', {'form': form, 'post': post})


@login_required
def hashtag_posts(request, hashtag_name):
    """Display posts with a specific hashtag"""
    hashtag = get_object_or_404(Hashtag, name=hashtag_name.lower())
    
    # Get posts with this hashtag that the user can view
    posts = hashtag.posts.filter(
        Q(user=request.user) | Q(is_public=True)
    ).select_related('user', 'user__profile').prefetch_related('hashtags', 'likes', 'comments')
    
    # Filter out private posts from users the current user doesn't follow
    viewable_posts = []
    for post in posts:
        if post.can_user_view(request.user):
            viewable_posts.append(post)
    
    paginator = Paginator(viewable_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get trending hashtags for sidebar
    trending_hashtags = Hashtag.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0).order_by('-post_count')[:10]
    
    context = {
        'hashtag': hashtag,
        'page_obj': page_obj,
        'trending_hashtags': trending_hashtags,
    }
    return render(request, 'posts/hashtag_posts.html', context)


@login_required
def trending_hashtags(request):
    """Display trending hashtags"""
    # Get hashtags with post count and recent activity
    trending_hashtags = Hashtag.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0).order_by('-post_count')[:20]
    
    # Calculate trending score for each hashtag
    for hashtag in trending_hashtags:
        hashtag.trending_score = hashtag.get_trending_score()
    
    # Sort by trending score
    trending_hashtags = sorted(trending_hashtags, key=lambda x: x.trending_score, reverse=True)
    
    context = {
        'trending_hashtags': trending_hashtags,
    }
    return render(request, 'posts/trending_hashtags.html', context)


@login_required
def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        # Check if query is a hashtag
        if query.startswith('#'):
            hashtag_name = query[1:].lower()
            try:
                hashtag = Hashtag.objects.get(name=hashtag_name)
                return redirect('posts:hashtag_posts', hashtag_name=hashtag_name)
            except Hashtag.DoesNotExist:
                posts = Post.objects.none()
        else:
            # Search in content, username, and hashtags
            posts = Post.objects.filter(
                Q(content__icontains=query) | 
                Q(user__username__icontains=query) |
                Q(hashtags__name__icontains=query)
            ).filter(is_public=True).select_related('user', 'user__profile').distinct()
    else:
        posts = Post.objects.none()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'posts/search_results.html', context)


@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(is_read=False).count()
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.POST.get('mark_all_read'):
            # Mark all notifications as read
            notifications.filter(is_read=False).update(is_read=True)
            return JsonResponse({'success': True, 'unread_count': 0})
        elif request.POST.get('notification_id'):
            # Mark specific notification as read
            notification_id = request.POST.get('notification_id')
            try:
                notification = notifications.get(pk=notification_id)
                notification.is_read = True
                notification.save()
                return JsonResponse({'success': True})
            except:
                return JsonResponse({'success': False}, status=400)
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'posts/notifications.html', context)
