from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, CourseForm, SubjectForm, TopicForm, TimeTableForm, StudySessionForm, StudyLogForm
from .models import Course, Subject, Topic, Progress
import datetime

import json

from django.contrib.auth.models import User

# Creating an admin user
admin_user = User.objects.create_user(username="admin", password="admin123")
admin_user.is_staff = True  # Set as admin
admin_user.save()

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after registration
            return redirect("dashboard")  # Redirect to dashboard after signup
    else:
        form = RegisterForm()

    return render(request, "scheduler/register.html", {"form": form})
def user_login(request):
    """Handles user login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect('dashboard')  # Change 'dashboard' to your home page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    
    form = AuthenticationForm()
    return render(request, 'scheduler/login.html', {'form': form})

def user_logout(request):
    """Handles user logout"""
    if request.method == "POST" or request.method == "GET":
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')  # Redirect to login page after logout

@login_required
def add_user(request):
    """ Allow only admins to add users """
    if not request.user.is_staff:
        messages.error(request, "Only admins can add users.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Normal user
            user.save()
            messages.success(request, "User added successfully!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'scheduler/add_user.html', {'form': form})


@login_required(login_url="/login/") 
def dashboard(request):
    return render(request, 'scheduler/dashboard.html')

@login_required
def course_view(request):
    courses = Course.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request, 'scheduler/course.html', {'form': form, 'courses': courses})

@login_required
def subject_view(request):
    subjects = Subject.objects.filter(course__user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SubjectForm()
    return render(request, 'scheduler/subject.html', {'form': form, 'subjects': subjects})

@login_required
def topic_view(request):
    topics = Topic.objects.filter(subject__course__user=request.user)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TopicForm()
    return render(request, 'scheduler/topic.html', {'form': form, 'topics': topics})

def progress_view(request):
    # Convert QuerySet to a list of dictionaries
    progress_data = list(Progress.objects.values("date", "hours_studied"))
    
    return render(request, "scheduler/progress.html", {"progress": progress_data})


@login_required
def select_course(request):
    courses = Course.objects.all()
    
    if request.method == "POST":
        course_id = request.POST.get("course")
        request.session["selected_course"] = course_id  # Store selection in session
        return redirect("select_subject")  # Redirect to subject selection
    
    return render(request, "scheduler/select_course.html", {"courses": courses})


@login_required
def select_subject(request):
    course_id = request.session.get("selected_course")
    if not course_id:
        return redirect("select_course")  # Redirect if no course selected
    
    subjects = Subject.objects.filter(course_id=course_id)
    
    if request.method == "POST":
        subject_id = request.POST.get("subject")
        request.session["selected_subject"] = subject_id  # Store selection in session
        return redirect("select_topic")  # Redirect to topic selection
    
    return render(request, "scheduler/select_subject.html", {"subjects": subjects})

@login_required
def select_topic(request):
    subject_id = request.session.get("selected_subject")
    if not subject_id:
        return redirect("select_subject")  # Redirect if no subject selected
    
    topics = Topic.objects.filter(subject_id=subject_id)
    
    if request.method == "POST":
        topic_id = request.POST.get("topic")
        request.session["selected_topic"] = topic_id  # Store selection in session
        return redirect("add_study_time")  # Redirect to log study time
    
    return render(request, "scheduler/select_topic.html", {"topics": topics})

@login_required
def add_study_time(request):
    topic_id = request.session.get("selected_topic")
    if not topic_id:
        return redirect("select_topic")  # Redirect if no topic selected

    topic = Topic.objects.get(id=topic_id)

    if request.method == "POST":
        form = StudyLogForm(request.POST)
        if form.is_valid():
            study_log = form.save(commit=False)
            study_log.user = request.user
            study_log.topic = topic
            study_log.save()
            return redirect("progress")  # Redirect to progress tracking
    
    else:
        form = StudyLogForm()
    
    return render(request, "scheduler/add_study_time.html", {"form": form, "topic": topic})
