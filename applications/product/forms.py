from django import forms
from .models import Favorite
from .models import Product

class form_favorite(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = (
            'user',
            'product',
        )
        
class SubirCSVForm(forms.Form):
    archivo_csv = forms.FileField()
    


class TuFormulario(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name_product', 'description_product', 'price_product', 'quantity_product', 'code_product', 'categories_product', 'image_product']
