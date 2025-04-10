from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    
class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    hours_spent = models.FloatField(default=0.0)  # Custom time entry in hours

    def __str__(self):
        return self.name

    def set_time_spent(self, hours, minutes):
        """Allows users to manually enter hours and minutes as time spent."""
        total_hours = hours + (minutes / 60)  # Convert minutes to hours
        self.hours_spent = round(total_hours, 2)  # Store rounded float value
        self.save()
        
class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.topic.name} - {self.date}"
