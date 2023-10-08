from django.db import models
from applications.seller.models import Seller
class Notification(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
