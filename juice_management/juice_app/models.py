from django.db import models

# Juice Product Model
class JuiceProduct(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Inventory Model
class Inventory(models.Model):
    product = models.ForeignKey(JuiceProduct, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.stock_quantity} left"

# Sales Model
class Sales(models.Model):
    product = models.ForeignKey(JuiceProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.product and self.quantity:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
