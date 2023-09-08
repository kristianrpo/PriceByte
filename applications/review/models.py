from django.db import models

class Rating(models.Model):
    garantia = models.IntegerField()
    precio  = models.IntegerField()
    calidad  = models.IntegerField()