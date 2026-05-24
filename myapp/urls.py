"""
URL configuration for chidiyaa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('reels/', views.reels, name='reels'),
    path('messages/', views.messages, name='messages'),
    path('messages/<int:pk>/', views.messages, name='messages_chat'),
    path('notifications/', views.notifications, name='notifications'),
    path('create/', views.create, name='create'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('following/', views.following, name='following'),
    path('follow_unfollow/<int:pk>', views.follow_unfollow, name='follow_unfollow'),
    path('followers/', views.followers, name='followers'),
    path('upload_reels/', views.upload_reels, name='upload_reels'),
    path('post_like/<int:pk>', views.post_like, name='post_like'),
    path('post_comment/<int:pk>', views.post_comment, name='post_comment'),
    path('comment_view/<int:pk>', views.comment_view, name='comment_view'),


    path('user_profile/<int:pk>', views.user_profile, name='user_profile'),
    path('user_following/<int:pk>', views.user_following, name='user_following'),
    path('user_followers/<int:pk>', views.user_followers, name='user_followers'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('otp/', views.otp, name='otp'),


]