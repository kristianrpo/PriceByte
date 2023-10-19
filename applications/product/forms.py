from django import forms
from .models import Favorite

class form_favorite(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = (
            'user',
            'product',
        )
        
class SubirCSVForm(forms.Form):
    archivo_csv = forms.FileField()