from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'location', 'get_followers_count', 'get_following_count', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['user__username', 'user__email', 'bio', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_followers_count(self, obj):
        return obj.get_followers_count()
    get_followers_count.short_description = 'Followers'
    
    def get_following_count(self, obj):
        return obj.get_following_count()
    get_following_count.short_description = 'Following'
