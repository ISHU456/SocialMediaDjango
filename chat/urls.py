from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('room/<int:conversation_id>/', views.chat_room, name='chat_room'),
    path('start/<str:username>/', views.start_conversation, name='start_conversation'),
    path('send/<int:conversation_id>/', views.send_message, name='send_message'),
    path('messages/<int:conversation_id>/', views.get_messages, name='get_messages'),
    path('unread-count/', views.get_unread_count, name='get_unread_count'),
    path('search/', views.search_users, name='search_users'),
] 