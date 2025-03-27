from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.homepage, name="home"),  # Example home route
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('portfolio/', views.portfolio, name='portfolio'),  # Add this line
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="agency/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)