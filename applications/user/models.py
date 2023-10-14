from django.db import models

class Client(models.Model):
    email_client = models.CharField(("email"),max_length=70)
    Name = models.CharField(("name"), max_length=20)
    def __str__(self):
        return str(self.Name)