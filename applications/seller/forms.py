from django import forms
from applications.product.models import Product

class FormCreateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name_product', 'description_product', 'price_product', 'quantity_product', 'code_product', 'categories_product')
        widgets = {
            'categories_product': forms.CheckboxSelectMultiple,
        }