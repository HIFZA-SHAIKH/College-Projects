from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Product, Sale, Invoice
from django.db.models import Sum
from .models import Sale, Customer, Product
from django.db.models import Sum, F
from .models import Product
from .forms import SaleForm  # Import SaleForm from the forms module

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'management/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    customers = Customer.objects.all()
    sales = Sale.objects.filter(id__isnull=False)
    invoices = Invoice.objects.all()
    p=Product.objects.all()
    
    return render(request, 'management/dashboard.html', {
        'customers': customers,
        'sales': sales,
        'invoices': invoices,
        'products':p
    })

@login_required
def add_customer(request):
    if request.method == "POST":
        Customer.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address']
        )
        return redirect('dashboard')
    return render(request, 'management/add_customer.html')

@login_required
def create_invoice(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    invoice, created = Invoice.objects.get_or_create(sale=sale)
    return redirect('view_invoices')

@login_required
def view_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'invoice.html', {'invoice': invoice})

@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        if name and description and price:
            Product.objects.create(
                name=name,
                description=description,
                price=price
            )
            return redirect('product_list')  # Redirect to product list page

    return render(request, 'management/add_product.html')




@login_required
def add_sale(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after adding a sale
    else:
        form = SaleForm()
    total_sales = Sale.objects.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0

    return render(request, 'management/add_sale.html', {'form': form})


@login_required
def view_sales(request):
    sales = Sale.objects.filter(id__isnull=False)  # Ensures only valid sales are shown
    return render(request, 'management/sales.html', {'sales': sales})

@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        if name and description and price:
            Product.objects.create(
                name=name,
                description=description,
                price=price
            )
            return redirect('product_list')  # Redirect to product list page

    return render(request, 'management/add_product.html')
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'management/product_list.html', {'products': products})

