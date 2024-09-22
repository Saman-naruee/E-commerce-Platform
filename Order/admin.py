from django.contrib import admin
from .models import Order, OrderItem
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'placed_at', 'payment_status']
    list_editable = ['payment_status']
    search_fields = ['payment_status']
    autocomplete_fields = ['user_profile']
    inlines = [OrderItemInline]
    list_per_page = 20


