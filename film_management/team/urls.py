from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

urlpatterns = [
   
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),    path('add-team-member/', views.add_team_member, name='add_team_member'),
    path('add-project/', views.add_project, name='add_project'),
    path('add-task/', views.add_task, name='add_task'),
    path('dashboard/', views.dashboard, name='dashboard')
]
