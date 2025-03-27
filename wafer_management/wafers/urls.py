from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.order_list, name='order_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    
    path('add-category/', views.add_category, name='add_category'),
  
    path('add-customer/', views.add_customer, name='add_customer'),
    path('add-product/',  views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-order/', views.add_order, name='add_order'),
    path('update-order-status/<int:order_id>/',views.update_order_status, name="update_order_status"),


     
]
