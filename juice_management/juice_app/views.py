from django.shortcuts import render, redirect
from .models import JuiceProduct, Inventory, Sales
from .forms import ProductForm, InventoryForm
from django.contrib.auth.decorators import login_required
from django.db import models
from .forms import SalesForm 


# Home page
def home(request):
    return render(request, "juice_app/home.html")

# Juice Products List with Add Option
@login_required
def product_list(request):
    products = JuiceProduct.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "juice_app/product_list.html", {"products": products, "form": form})

# Inventory List with Update Option
@login_required
def inventory_list(request):
    inventory = Inventory.objects.all()
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory_list")
    else:
        form = InventoryForm()
    return render(request, "juice_app/inventory_list.html", {"inventory": inventory, "form": form})

# Sales List with Process Sale Option
@login_required
def sales_list(request):
    sales = Sales.objects.all()
    form = SalesForm()

    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            product = sale.product
            inventory = Inventory.objects.filter(product=product).first()

            if inventory and sale.quantity <= inventory.stock_quantity:
                # Deduct stock and save sale
                inventory.stock_quantity -= sale.quantity
                inventory.save()
                sale.save()
                return redirect('sales_list')
            else:
                return render(request, 'juice_app/sales_list.html', {
                    'sales': sales, 'form': form, 'error': 'Not enough stock available!'
                })

    return render(request, 'juice_app/sales_list.html', {'sales': sales, 'form': form})


@login_required
def dashboard(request):
    return render(request, 'juice_app/dashboard.html')
