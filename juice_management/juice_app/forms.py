from django import forms
from .models import JuiceProduct, Inventory, Sales

# Form for adding a Juice Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = JuiceProduct
        fields = ['name', 'category', 'price', 'description']

# Form for updating Inventory
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'stock_quantity']

# Form for processing a sale

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['product', 'quantity']
