from typing import Any
from django.contrib import admin
from django.contrib import admin, messages
from .models import Product
from Tag.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline


class ProductInventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>30', 'Ok'), 
        ]
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>30':
            return queryset.filter(inventory__gt=30)


class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'collection', 'inventory_status', 'inventory']    
    list_per_page = 20
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', ProductInventoryFilter]
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.display(description='Clear Inventory.')
    def clear_inventory(self, request, queryset):
        inventory_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{inventory_count} products were successfully updated.',
            messages.SUCCESS
        )

class TaggedInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedInline]

admin.site.register(Product, CustomProductAdmin)
