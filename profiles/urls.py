from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.suggested_users, name='suggested_users'),
    path('user/<str:username>/', views.profile_view, name='profile_view'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('user/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('user/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('user/<str:username>/following/', views.following_list, name='following_list'),
    path('search/', views.search_users, name='search_users'),
] 