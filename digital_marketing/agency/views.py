from django.shortcuts import render, redirect
from .models import Service, Testimonial, Blog, Portfolio
from .forms import ContactForm
from .models import ContactMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test

def homepage(request):
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()
    blogs = Blog.objects.order_by('-created_at')[:3]
    return render(request, 'agency/home.html', {'services': services, 'testimonials': testimonials, 'blogs': blogs})

def contact(request):
    return render(request, 'agency/contact.html')

def about(request):
    return render(request, 'agency/about.html')

def portfolio(request):
    return render(request, 'agency/portfolio.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send email notification
            send_mail(
                subject=f"New Inquiry from {contact_message.name}",
                message=f"Subject: {contact_message.subject}\n\nMessage:\n{contact_message.message}\n\nFrom: {contact_message.email}",
                from_email="your_email@gmail.com",
                recipient_list=["your_email@gmail.com"],  # Replace with admin email
            )

            return redirect("contact_success")  # Redirect to success page

    else:
        form = ContactForm()

    return render(request, "agency/contact.html", {"form": form})

def contact_success(request):
    return render(request, "agency/contact_success.html")

@login_required
def admin_dashboard(request):
    total_inquiries = ContactMessage.objects.count()
    latest_inquiries = ContactMessage.objects.order_by('-created_at')[:5]

    context = {
        "total_inquiries": total_inquiries,
        "latest_inquiries": latest_inquiries,
    }
    return render(request, "agency/dashboard.html", context)

def is_admin(user):
    return user.is_authenticated and user.is_staff

# Restrict access to admin or staff only
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_inquiries = ContactMessage.objects.count()
    latest_inquiries = ContactMessage.objects.order_by('-created_at')[:5]

    context = {
        "total_inquiries": total_inquiries,
        "latest_inquiries": latest_inquiries,
    }
    return render(request, "agency/dashboard.html", context)

def portfolio(request):
    projects = Portfolio.objects.all()
    return render(request, "agency/portfolio.html", {"projects": projects})