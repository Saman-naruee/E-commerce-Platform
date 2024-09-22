from django.contrib import admin
from Product.admin import ProductAdmin
from Product.models import Product
from Tag.models import TaggedItem
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Count

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


class TaggedInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']

class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 20
    search_fields = ['user_first_name', 'user_last_name', 'first_name__istartswith', 'last_name__istartswith']
    list_select_related = ['user']
    autocomplete_fields = ['user']
    @admin.display(ordering='order_count')
    def order_count(self, user):
        related_url = reverse('admin:store_order_changelist')\
        + '?' + urlencode({
            'customer_id': str(user.pk)
        })
        return format_html(f'<a href="{related_url}">{user.order_count}</a>')
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )