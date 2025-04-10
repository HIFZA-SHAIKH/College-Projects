from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Course, Subject, Topic, Timetable, CustomUser
from .forms import CourseForm, SubjectForm, TopicForm, TimetableForm, UserRegistrationForm, LoginForm
from django.utils.timezone import now


def home(request):
    return render(request, 'scheduler/home.html')  # Renders home page
# Admin Dashboard
@login_required
def admin_dashboard(request):
    return render(request, 'scheduler/admin_dashboard.html')

# User Dashboard
@login_required
def user_dashboard(request):
    courses = Course.objects.all()
    subjects = []
    topics = []

    selected_course_id = request.GET.get('course_id')
    selected_subject_id = request.GET.get('subject_id')

    selected_course = None
    selected_subject = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)
        subjects = Subject.objects.filter(course=selected_course)

    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id)
        topics = Topic.objects.filter(subject=selected_subject)

    return render(request, 'scheduler/user_dashboard.html', {
        'courses': courses,
        'subjects': subjects,
        'topics': topics,
        'selected_course': selected_course,
        'selected_subject': selected_subject,
        'selected_course_id': selected_course_id,
        'selected_subject_id': selected_subject_id,
    })

# Add Course (Admin Only)
@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'scheduler/add_course.html', {'form': form})

# Add Subject (Admin Only)
@login_required
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = SubjectForm()
    return render(request, 'scheduler/add_subject.html', {'form': form})

# Add Topic (Admin Only)
@login_required
@login_required
def add_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # ✅ Fix redirection here
    else:
        form = TopicForm()
    return render(request, 'scheduler/add_topic.html', {'form': form})
# Mark Topic as Done (Users)
@login_required
def mark_done(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if topic.start_time is None:
        topic.start_time = now()  # Record start time

    topic.end_time = now()  # Set end time when completed
    topic.is_completed = True

    # Calculate time spent in hours
    time_spent = (topic.end_time - topic.start_time).total_seconds() / 3600
    topic.hours_spent = round(time_spent, 2)  # Store in hours

    topic.save()
    return redirect('user_dashboard')  # Reload dashboard
# User Progress
@login_required
def user_progress(request):
    # Get all topics
    topics = Topic.objects.all()

    # Count completed and total topics
    completed_topics = topics.filter(is_completed=True).count()
    total_topics = topics.count()

    # Calculate total hours spent
    total_hours_spent = sum(topic.hours_spent for topic in topics)

    # Calculate progress percentage
    progress = (completed_topics / total_topics) * 100 if total_topics > 0 else 0

    return render(request, 'scheduler/progress_chart.html', {
        'progress': progress,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
        'total_hours_spent': total_hours_spent
    })

# User Registration
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['is_admin']:
                user.is_admin = True
            user.save()
            return redirect('login')  # Redirect to login page
    else:
        form = UserRegistrationForm()
    return render(request, 'scheduler/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on user type
            if user.is_admin:
                return redirect('admin_dashboard')  # Admin Redirect
            else:
                return redirect('user_dashboard')  # User Redirect

    else:
        form = LoginForm()
    return render(request, 'scheduler/login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_timetable(request):
    if request.method == "POST":
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect after saving
    else:
        form = TimetableForm()
    return render(request, 'scheduler/add_timetable.html', {'form': form})