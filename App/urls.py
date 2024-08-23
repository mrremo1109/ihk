from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registerRecruiter/', views.registerRecruiter, name='registerRecruiter'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('profile/', views.profile, name='profile'),
    path('logoutUser/', views.logoutuser, name='logoutUser'),
    path('apply/<str:job_id>', views.apply, name='apply'),
    path('addPost/' , views.addPost, name='addPost'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
    path('search/', views.searched, name='search'),
    path('manage_applications/', views.manage_applications, name='manage_applications'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('application/<int:application_id>/update/', views.update_application_status, name='update_application_status'),
    path('accept_application/<int:application_id>/', views.accept_application, name='accept_application'),
    path('reject_application/<int:application_id>/', views.reject_application, name='reject_application'),
    path('chat/', views.chat_view, name='chat_view'),  # This should be the general chat view URL
    path('chat/<str:email>/', views.chat_view, name='chat_view'),  # This should be for specific chat view
    path('send_message/', views.send_message, name='send_message'),
    ]