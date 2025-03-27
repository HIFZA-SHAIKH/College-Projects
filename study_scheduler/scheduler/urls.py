from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path("login/", auth_views.LoginView.as_view(template_name="scheduler/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),  # Ensure this function exists in views.py
    path('dashboard/', views.dashboard, name='dashboard'),
    path('progress/', views.progress_view, name='progress'),

    
    # Admin URLs
    path('course/', views.course_view, name='course'),
    path('subject/', views.subject_view, name='subject'),
    path('topic/', views.topic_view, name='topic'),
    path('add-user/', views.add_user, name='add_user'),

    # User URLs
    path('select-course/', views.select_course, name='select_course'),
    path('select-subject/', views.select_subject, name='select_subject'),
    path('select-topic/', views.select_topic, name='select_topic'),
    path('add-study-time/', views.add_study_time, name='add_study_time'),
    path('progress/', views.progress_view, name='progress'),
]

