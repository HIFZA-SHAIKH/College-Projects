from django import forms
from .models import TeamMember, Project, Task
from django.contrib.auth.forms import AuthenticationForm

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Select Start Date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Select End Date'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'assigned_to', 'task_name', 'status', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Select Due Date'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
