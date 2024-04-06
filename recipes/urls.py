from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"), 
    path('', views.about, name="about"), 


    
    path('login/',views.user_login, name='login'),
    path('logout/', views.logout, name ='logoutt'),
    path('signup/', views.signup, name ='signup'),
    path('upload/',views.upload,name='upload'),
    path('viewuploaded/',views.viewuploaded,name='viewuploaded'),
    path('user_data/',views.user_data,name='user_data'),

    
     path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
     
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),


]

