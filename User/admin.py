from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 20
    search_fields = ['user__first_name', 'user__last_name', 'first_name__istartswith', 'last_name__istartswith']
    list_select_related = ['user']
    autocomplete_fields = ['user']
    @admin.display(ordering='order_count')
    def order_count(self, user):
        related_url = reverse('admin:store_order_changelist')\
        + '?' + urlencode({
            'customer_id': str(user.user.pk)
        })
        return format_html(f'<a href="{related_url}">{user.order_count}</a>')
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )