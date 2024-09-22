from django.db import models
from Category.models import Category
from django.core.validators import MinValueValidator

class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, default='')
    discount = models.FloatField(default=0)

    def __str__(self) -> str:
        return str(self.discount)


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
                validators=[MinValueValidator(0)], 
                max_digits=6,
                decimal_places=2
            )
    inventory = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    discounts = models.ManyToManyField(Discount, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']