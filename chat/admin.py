from django.contrib import admin
from .models import Conversation, Message, ChatNotification


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_participants', 'created_at', 'updated_at', 'get_message_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['participants__username', 'participants__email']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_participants(self, obj):
        return ', '.join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'
    
    def get_message_count(self, obj):
        return obj.messages.count()
    get_message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'conversation', 'content_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at', 'sender']
    search_fields = ['sender__username', 'content', 'conversation__participants__username']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(ChatNotification)
class ChatNotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'conversation', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at', 'recipient', 'sender']
    search_fields = ['recipient__username', 'sender__username']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
