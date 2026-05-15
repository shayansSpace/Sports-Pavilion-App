from django.contrib import admin
from django.urls import path, include
from club_app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('members', views.member_list, name='member_list'),
    path('members/<int:member_id>/', views.member_profile, name='member_profile'),
]
