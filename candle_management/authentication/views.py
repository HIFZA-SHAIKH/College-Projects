from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, SupplierForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required
from .models import RawMaterial, FinishedGoods, ProductionBatch
from .forms import RawMaterialForm
from .models import StockAlert

def is_admin_or_production(user):
    return user.is_authenticated and (user.role == "admin" or user.role == "production")

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")  # Redirect after login
    else:
        form = RegistrationForm()
    return render(request, "authentication/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Make sure 'dashboard' exists in URLs
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')  # Redirect back to login if invalid
    
    return render(request, 'authentication/login.html')
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, 'authentication/dashboard.html')

@login_required
def raw_material_list(request):
    raw_materials = RawMaterial.objects.all()
    return render(request, "raw_materials/list.html", {"raw_materials": raw_materials})

@login_required
def add_raw_material(request):
    if request.user.role != 'admin':  # Only Admins can add materials
        return redirect('raw_material_list')

    if request.method == "POST":
        form = RawMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("raw_material_list")
    else:
        form = RawMaterialForm()
    return render(request, "raw_materials/form.html", {"form": form, "action": "Add"})

@login_required
def edit_raw_material(request, material_id):
    if request.user.role != 'admin':  # Only Admins can edit
        return redirect('raw_material_list')

    material = get_object_or_404(RawMaterial, id=material_id)
    if request.method == "POST":
        form = RawMaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect("raw_material_list")
    else:
        form = RawMaterialForm(instance=material)
    return render(request, "raw_materials/form.html", {"form": form, "action": "Edit"})

@login_required
def delete_raw_material(request, material_id):
    if request.user.role != 'admin':  # Only Admins can delete
        return redirect('raw_material_list')

    material = get_object_or_404(RawMaterial, id=material_id)
    material.delete()
    return redirect("raw_material_list")

@login_required
def stock_alerts_list(request):
    if request.user.role == 'admin'or request.user.role == 'production'or request.user.role =='sales':  #allow all roles to view alerts
        alerts = StockAlert.objects.filter(assigned_to=request.user)
        return render(request, "inventory/alerts.html", {"alerts": alerts})
    
@login_required
def update_raw_material_stock(request, material_id):
    """Only Production Team can update raw material stock."""
    if request.user.role != 'production':
        messages.error(request, "Unauthorized access!")
        return redirect("dashboard")

    material = get_object_or_404(RawMaterial, id=material_id)
    
    if request.method == "POST":
        used_quantity = int(request.POST.get("used_quantity", 0))
        if used_quantity > material.quantity:
            messages.error(request, "Not enough stock available!")
        else:
            material.quantity -= used_quantity
            material.save()
            messages.success(request, "Raw Material Stock Updated Successfully!")
        return redirect("raw_material_list")

    return render(request, "inventory/update_raw_material.html", {"material": material})


@login_required
def update_finished_goods_stock(request, goods_id):
    """Only Sales Team can update finished goods stock."""
    if request.user.role != 'sales':
        messages.error(request, "Unauthorized access!")
        return redirect("dashboard")

    finished_goods = get_object_or_404(FinishedGoods, id=goods_id)

    if request.method == "POST":
        added_quantity = int(request.POST.get("added_quantity", 0))
        finished_goods.quantity += added_quantity
        finished_goods.save()
        messages.success(request, "Finished Goods Stock Updated Successfully!")
        return redirect("finished_goods_list")

    return render(request, "inventory/update_finished_goods.html", {"goods": finished_goods})


@login_required
def sales_reports_view(request):
    return render(request, "sales_reports.html")  

@login_required
@user_passes_test(is_admin_or_production)
def create_production_batch(request):
    if request.method == "POST":
        batch_name = request.POST["batch_name"]
        batch_size = request.POST["batch_size"]
        time_taken = request.POST["time_taken"]
        batch = ProductionBatch.objects.create(
            batch_name=batch_name,
            batch_size=batch_size,
            time_taken=time_taken,
            created_by=request.user
        )
        return redirect("production_reports")
    return render(request, "production/create_batch.html")

@login_required
@user_passes_test(is_admin_or_production)
def edit_production_batch(request, batch_id):
    batch = get_object_or_404(ProductionBatch, id=batch_id)
    if request.method == "POST":
        batch.batch_name = request.POST["batch_name"]
        batch.batch_size = request.POST["batch_size"]
        batch.time_taken = request.POST["time_taken"]
        batch.save()
        return redirect("production_reports")
    return render(request, "production/edit_batch.html", {"batch": batch})

@login_required
@user_passes_test(is_admin_or_production)
def delete_production_batch(request, batch_id):
    batch = get_object_or_404(ProductionBatch, id=batch_id)
    batch.delete()
    return redirect("production_reports")

@login_required
@user_passes_test(is_admin_or_production)
def production_reports(request):
    batches = ProductionBatch.objects.all()
    return render(request, "production/reports.html", {"batches": batches})

@login_required
def add_supplier(request):
  if request.user.role == 'admin':  
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.added_by = request.user  # Assign the logged-in admin
            supplier.save()
            return redirect('add_raw_material')  # Redirect to raw material form
    else:
        form = SupplierForm()
    
    return render(request, 'authentication/supplier_form.html', {'form': form})