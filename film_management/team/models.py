from django.db import models

# Create your models here.
from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.title

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    due_date = models.DateField()
    
    def __str__(self):
        return self.task_name
