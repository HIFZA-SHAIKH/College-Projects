from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Category, Order, Customer
from .forms import CustomerForm, ProductForm, OrderForm, CategoryForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit

# Product List
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'wafers/product_list.html', {'products': products})

# Order List
@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'wafers/order_list.html', {'orders': orders})

# Customer List
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'wafers/customer_list.html', {'customers': customers})

# Generate Invoice
@login_required
def generate_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    html = render_to_string('wafers/invoice.html', {'order': order})
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    return response

# Dashboard with Forms
def dashboard(request):
    customer_form = CustomerForm()
    product_form = ProductForm()
    order_form = OrderForm()
    category_form = CategoryForm()

    if request.method == "POST":
        if "add_customer" in request.POST:
            customer_form = CustomerForm(request.POST)
            if customer_form.is_valid():
                customer_form.save()
                messages.success(request, "Customer added successfully!")
                return redirect("dashboard")

        elif "add_product" in request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, "Product added successfully!")
                return redirect("dashboard")

        elif "place_order" in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order_form.save()
                messages.success(request, "Order placed successfully!")
                return redirect("dashboard")

        elif "add_category" in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Category added successfully!")
                return redirect("dashboard")

    orders = Order.objects.all().order_by("-id")  # Fetch recent orders

    context = {
        "customer_form": customer_form,
        "product_form": product_form,
        "order_form": order_form,
        "category_form": category_form,
        "orders": orders,
    }
    return render(request, "wafers/dashboard.html", context)# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    
    return render(request, 'wafers/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category, created = Category.objects.get_or_create(name=name)
            if created:
                messages.success(request, 'Category added successfully!')
            else:
                messages.warning(request, 'Category already exists.')
            return redirect('add_category')

    return render(request, 'wafers/add_category.html')

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('dashboard')
    else:
        form = CustomerForm()
    return render(request, 'wafers/customer_list.html', {'form': form})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'wafers/product_list.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category, created = Category.objects.get_or_create(name=name)
            if created:
                messages.success(request, 'Category added successfully!')
            else:
                messages.warning(request, 'Category already exists.')
            return redirect('dashboard')
    return render(request, 'wafers/add_category.html')

def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order placed successfully!')
            return redirect('dashboard')
    else:
        form = OrderForm()
    return render(request, 'wafers/add_order.html', {'form': form})

def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        order.status = request.POST.get("status")
        order.save()
    return redirect("dashboard") 
