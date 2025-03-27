from django.shortcuts import render, redirect
from .models import TeamMember, Project, Task
from .forms import TeamMemberForm, ProjectForm, TaskForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'team/login.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def dashboard(request):
    members = TeamMember.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    return render(request, 'team/dashboard.html', {'members': members, 'projects': projects, 'tasks': tasks})

# Team Member Views
@login_required
def add_team_member(request):
    if request.method == "POST":
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TeamMemberForm()
    return render(request, 'team/add_member.html', {'form': form})

# Project Views
from django.shortcuts import render, redirect
from .forms import ProjectForm

@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect after submission
    else:
        form = ProjectForm()

    return render(request, 'team/add_project.html', {'form': form})


# Task Views
@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect after submission
    else:
        form = TaskForm()

    return render(request, 'team/add_task.html', {'form': form})
