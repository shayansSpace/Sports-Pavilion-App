from django.urls import path
from club_app import views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('book-visitor/', views.book_visitor, name='book_visitor'),
    path('become-member/', views.become_member, name='become_member'),
    path('book-member/', views.book_member, name='book_member'),
    
    # === ADMIN DASHBOARD - MEMBERS ===
    path('members/', views.member_list, name='member_list'),
    path('members/profile/<int:member_id>/', views.member_profile, name='member_profile'),
    path('members/add/', views.member_upsert, name='add_member'),
    path('members/edit/<int:member_id>/', views.member_upsert, name='edit_member'),
    path('members/delete/<int:member_id>/', views.delete_member, name='delete_member'),

    # === ADMIN DASHBOARD - STAFF ===
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.staff_create, name='staff_create'),
    path('staff/edit/<int:staff_id>/', views.staff_update, name='staff_update'),
    path('staff/delete/<int:staff_id>/', views.staff_delete, name='staff_delete'),
]