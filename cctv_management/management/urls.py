from django.urls import path
from .views import dashboard, add_customer, create_invoice, login_view, logout_view,view_invoice,add_sale,view_invoice
from django.contrib.auth import views as auth_views
from .views import add_product,product_list,view_sales

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='management/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),

    path('add-customer/', add_customer, name='add_customer'),
    path('create-invoice/<int:sale_id>/', create_invoice, name='create_invoice'),  # Ensure sale_id is an integer
    path('invoice/<int:invoice_id>/', view_invoice, name='view_invoice'),  # Ensure invoice_id is passed
    path('add-sale/', add_sale, name='add_sale'),
    path('sales/', view_sales, name='view_sales'),
    path('view-invoices/', view_invoice, name='view_invoices'),
    path('add-product/', add_product, name='add_product'),
    path('products/', product_list, name='product_list'),


]
