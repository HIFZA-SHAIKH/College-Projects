from django.contrib import admin
from .models import Service, Testimonial, Blog, Inquiry, Portfolio

admin.site.register(Service)
admin.site.register(Testimonial)
admin.site.register(Blog)
admin.site.register(Inquiry)
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")