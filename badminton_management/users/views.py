from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import role_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Court, CourtBooking
from .forms import CourtForm, CourtBookingForm
from .decorators import role_required
from django.contrib import messages



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')  # Redirect to dashboard
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

@login_required
@role_required(['player'])
def player_dashboard(request):
    return render(request, 'users/player_dashboard.html')


@login_required
def dashboard(request):
    if request.user.role == 'admin':
        all_bookings = CourtBooking.objects.all()
    else:
        all_bookings = None  # Admin only

    user_bookings = CourtBooking.objects.filter(user=request.user)

    return render(request, 'users/dashboard.html', {
        'all_bookings': all_bookings,
        'user_bookings': user_bookings,
    })


@login_required
@role_required(['admin'])
def add_court(request):
    if request.method == "POST":
        form = CourtForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Court added successfully.")
            return redirect('dashboard')
    else:
        form = CourtForm()
    return render(request, 'users/add_court.html', {'form': form})

# Player/Coach - Book Court
@login_required
@role_required(['player', 'coach'])
def book_court(request):
    if request.method == "POST":
        form = CourtBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Court booked successfully. Waiting for admin approval.")
            return redirect('dashboard')
    else:
        form = CourtBookingForm()
    return render(request, 'users/book_court.html', {'form': form})

# All Users - View Bookings
@login_required
def view_bookings(request):
    if request.user.role == "admin":
        bookings = CourtBooking.objects.all()
    else:
        bookings = CourtBooking.objects.filter(user=request.user)
    
    return render(request, 'users/view_bookings.html', {'bookings': bookings})

# Admin - Approve/Reject Booking
@login_required
@role_required(['admin'])
def manage_bookings(request):
    bookings = CourtBooking.objects.all()
    
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")
        booking = get_object_or_404(CourtBooking, id=booking_id)

        if action == "approve":
            booking.status = "Approved"
        elif action == "reject":
            booking.status = "Rejected"
        booking.save()
        messages.success(request, f"Booking {action}d successfully.")
        return redirect('manage_bookings')

    return render(request, 'users/manage_bookings.html', {'bookings': bookings})
