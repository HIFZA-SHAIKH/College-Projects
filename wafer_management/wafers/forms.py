from django import forms
from .models import Customer, Product, Order, Category

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")

    class Meta:
        model = Product
        fields = ['name', 'price', 'category','stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'quantity', 'status']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
