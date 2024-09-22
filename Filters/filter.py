from django_filters import FilterSet
from Product.models import Product
from Category.models import Category
"""
for more information:
    https://django-filter.readthedocs.io/en/stable/
learn : generic filters.
"""
class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt']
        }

class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'title': ['exact'],
            'featured_product': ['exact']
        }