from django.db import models
from mptt.models import MPTTModel, TreeForeignKey  

class Category(MPTTModel):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='product', blank=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')  
    attributes_schema = models.JSONField(default=dict) # Stores json schema  
    
    def __str__(self) -> str:
        return self.title

    class MPTTMeta:  
        order_insertion_by = ['title']  
