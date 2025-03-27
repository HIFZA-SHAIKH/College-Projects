from django.db import models
from ckeditor.fields import RichTextField

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=255)
    feedback = models.TextField()
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.client_name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Inquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Portfolio(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="portfolio/")
    project_url = models.URLField(blank=True, null=True)  # Optional project link
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title