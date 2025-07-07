from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('post/<int:pk>/share/', views.share_post, name='share_post'),
    path('search/', views.search_posts, name='search_posts'),
    path('hashtag/<str:hashtag_name>/', views.hashtag_posts, name='hashtag_posts'),
    path('trending/', views.trending_hashtags, name='trending_hashtags'),
    path('notifications/', views.notifications, name='notifications'),
] 