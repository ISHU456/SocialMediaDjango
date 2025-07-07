from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import re


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.name}"
    
    def get_absolute_url(self):
        return reverse('posts:hashtag_posts', kwargs={'hashtag_name': self.name})
    
    def get_posts_count(self):
        return self.posts.count()
    
    def get_trending_score(self):
        """Calculate trending score based on recent posts"""
        from django.utils import timezone
        from datetime import timedelta
        
        # Get posts from last 7 days
        week_ago = timezone.now() - timedelta(days=7)
        recent_posts = self.posts.filter(created_at__gte=week_ago)
        
        # Calculate score based on likes, comments, and shares
        total_engagement = 0
        for post in recent_posts:
            total_engagement += post.get_likes_count() + post.get_comments_count() + post.get_share_count()
        
        return total_engagement


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.pk})

    def get_likes_count(self):
        return self.likes.count()

    def get_comments_count(self):
        return self.comments.count()

    def get_share_count(self):
        return self.shares.count()
    
    def extract_hashtags(self):
        """Extract hashtags from content and create/update them"""
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, self.content)
        
        # Clear existing hashtags
        self.hashtags.clear()
        
        # Add new hashtags
        for hashtag_name in hashtags:
            hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name.lower())
            self.hashtags.add(hashtag)
    
    def save(self, *args, **kwargs):
        # Save the post first
        super().save(*args, **kwargs)
        # Extract and add hashtags
        self.extract_hashtags()
    
    def can_user_view(self, user):
        """Check if a user can view this post"""
        if self.user == user:  # Post owner can always view
            return True
        if self.is_public:  # Public posts can be viewed by anyone
            return True
        # Followers can view private posts
        return user in [profile.user for profile in self.user.profile.followers.all()]
    
    def can_user_interact(self, user):
        """Check if a user can interact with this post (like, comment, share)"""
        return self.can_user_view(user)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}..."

    def get_likes_count(self):
        return self.likes.count()

    def get_replies_count(self):
        return self.replies.count()


class Share(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)  # Optional comment when sharing

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} shared {self.post.user.username}'s post"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('share', 'Share'),
        ('mention', 'Mention'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} {self.notification_type} - {self.recipient.username}"

    def get_message(self):
        if self.notification_type == 'like':
            return f"{self.sender.username} liked your post"
        elif self.notification_type == 'comment':
            return f"{self.sender.username} commented on your post"
        elif self.notification_type == 'follow':
            return f"{self.sender.username} started following you"
        elif self.notification_type == 'share':
            return f"{self.sender.username} shared your post"
        elif self.notification_type == 'mention':
            return f"{self.sender.username} mentioned you in a comment"
        return "New notification"
