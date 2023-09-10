from django.db import models
from applications.product.models import Product
from applications.accounts.models import User
class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_rating = models.IntegerField()
    quality_rating = models.IntegerField()
    warranty_rating = models.IntegerField()
    description = models.TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Rating for {self.product.name_product}"
