from django.urls import path
from .views import register_view, login_view, logout_view, dashboard
from .views import raw_material_list, add_raw_material, edit_raw_material, delete_raw_material, stock_alerts_list, update_raw_material_stock, update_finished_goods_stock, sales_reports_view, delete_production_batch, edit_production_batch, create_production_batch, production_reports,add_supplier


urlpatterns = [
    path("register/", register_view, name="register"),
    path("alerts/", stock_alerts_list, name="stock_alerts"),

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("raw-materials/", raw_material_list, name="raw_material_list"),
    path("raw-materials/add/", add_raw_material, name="add_raw_material"),
    path('supplier/add/', add_supplier, name='add_supplier'),  
    path("raw-materials/edit/<int:material_id>/", edit_raw_material, name="edit_raw_material"),
    path("raw-materials/delete/<int:material_id>/", delete_raw_material, name="delete_raw_material"),
    path('update-raw-materials/<int:material_id>/', update_raw_material_stock, name='update_raw_material_stock'),
    path("update-finished-goods-stock/", update_finished_goods_stock, name="update_finished_goods_stock"),
    
    path("sales-reports/", sales_reports_view, name="sales_reports"),
     path("production/create/", create_production_batch, name="create_production_batch"),
    path("production/edit/<int:batch_id>/", edit_production_batch, name="edit_production_batch"),
    path("production/delete/<int:batch_id>/", delete_production_batch, name="delete_production_batch"),
    path("production/reports/", production_reports, name="production_reports"),

]
