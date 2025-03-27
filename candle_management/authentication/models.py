from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('production', 'Production Staff'),
        ('sales', 'Sales Team'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='production')

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Track which admin added the supplier

    def __str__(self):
        return self.name


class RawMaterial(models.Model):
    MATERIAL_TYPES = [
        ('wax', 'Wax'),
        ('wick', 'Wick'),
        ('fragrance_oil', 'Fragrance Oil'),
        ('dye', 'Dye'),
        ('mold', 'Mold'),
        ('other', 'Other')
    ]
    
    name = models.CharField(max_length=255)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    quantity_in_stock = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField(default=10)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  # Supplier is required

    def needs_reordering(self):
        return self.quantity_in_stock <= self.reorder_level

    def __str__(self):
        return f"{self.name} ({self.material_type})"

class FinishedGoods(models.Model):
    product_name = models.CharField(max_length=255)
    quantity_in_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name

class StockAlert(models.Model):
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Use this instead of 'auth.User'
        on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock Alert assigned to {self.assigned_to}"
    
class ProductionBatch(models.Model):
    batch_name = models.CharField(max_length=255)
    batch_size = models.IntegerField()
    time_taken = models.DurationField()
    workers_assigned = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="production_batches"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_batches"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.batch_name
