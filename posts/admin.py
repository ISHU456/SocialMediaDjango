from django.contrib import admin
from .models import Post, Comment, Share, Notification, Hashtag


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_posts_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    ordering = ['-created_at']
    
    def get_posts_count(self, obj):
        return obj.get_posts_count()
    get_posts_count.short_description = 'Posts Count'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_preview', 'created_at', 'is_public', 'get_likes_count', 'get_comments_count']
    list_filter = ['created_at', 'is_public']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['likes', 'hashtags']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
    
    def get_likes_count(self, obj):
        return obj.get_likes_count()
    get_likes_count.short_description = 'Likes'
    
    def get_comments_count(self, obj):
        return obj.get_comments_count()
    get_comments_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content_preview', 'created_at', 'get_likes_count']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content', 'post__content']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['likes']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def get_likes_count(self, obj):
        return obj.get_likes_count()
    get_likes_count.short_description = 'Likes'


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'sender__username']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
