from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('player', 'Player'),
        ('coach', 'Coach'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Court(models.Model):
    name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CourtBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")  # ✅ Update this line
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.court.name} ({self.booking_date})"
