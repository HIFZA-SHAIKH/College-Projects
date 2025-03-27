from django.db import models
from django.contrib.auth.models import AbstractUser

# Superuser model
class SuperUser(AbstractUser):
    # Prevent conflicts with auth.User
    groups = models.ManyToManyField(
        'auth.Group', related_name='superuser_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='superuser_permissions', blank=True
    )

    def __str__(self):
        return self.username

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.name

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.product.price

class Invoice(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.sale.customer.name} on {self.invoice_date}"
