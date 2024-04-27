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
    path('all_recipe/', views.all_recipe, name ='all_recipe'),
    path('show_all_recipe/', views.show_all_recipe, name='show_all_recipe'),


   
    path('upload/',views.upload,name='upload'),
    path('viewuploaded/',views.viewuploaded,name='viewuploaded'),
    path('user_data/',views.user_data,name='user_data'),    
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    
    
    
    
    
    path('send_for_approval/', views.send_for_approval, name='send_for_approval'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('submissions/',views.submissions,name='submissions'),
    path('submission_table/',views.submission_table,name='submission_table'),

    
    
    
    path('full_recipe/',views.full_recipe,name='full_recipe'),
    path('recipe_content/',views.recipe_content,name='recipe_content'),
    
    

    

    


]

