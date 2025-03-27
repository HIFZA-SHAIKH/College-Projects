from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name="juice_app/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('sales/', views.sales_list, name='sales_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
