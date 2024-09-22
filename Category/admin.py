from django.contrib import admin
from .models import Category
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Count


@admin.register(Category)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count'] # second field: to find out how many products we have related to collection.
    list_per_page = 20
    search_fields = ['title']
    autocomplete_fields = ['featured_product']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        # reverse('admin:app_model_page') target page links:
        related_url = reverse('admin:store_product_changelist')\
        + '?' + urlencode({
            'collection_id': str(collection.pk)
        })
        # make a value of a field to clickable and ralate to links.
        return format_html(f'<a href="{related_url}">{collection.product_count}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('products')
        )
 
