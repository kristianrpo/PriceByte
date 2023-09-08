from django.db import models

class Seller(models.Model):
    NIT_seller = models.CharField(("NIT"), max_length=20)
    name_company_seller = models.CharField(("name_company"), max_length=50)
    email_seller = models.CharField(("email"),max_length=70)
    phone_number_seller = models.CharField(("phone_number"), max_length=20)
    address = models.CharField(("address"), max_length=60)
    local_number_seller = models.CharField(("local_number_seller"),max_length=8)
    def __str__(self):
        return str(self.name_company_seller)