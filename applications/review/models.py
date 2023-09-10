from django.db import models
from applications.product.models import Product

class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_rating = models.IntegerField()
    quality_rating = models.IntegerField()
    warranty_rating = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return f"Rating for {self.product.name_product}"
