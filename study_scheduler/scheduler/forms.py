from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Subject, Topic, TimeTable, StudySession
from .models import StudyLog


class RegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'course']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'subject', 'completed']

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['subject', 'exam_date']

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['subject', 'duration']

class StudyLogForm(forms.ModelForm):
    class Meta:
        model = StudyLog
        fields = ["time_spent"]  # User inputs study time