from django.contrib import admin
from .models import JuiceProduct, Inventory, Sales

admin.site.register(JuiceProduct)
admin.site.register(Inventory)
admin.site.register(Sales)
