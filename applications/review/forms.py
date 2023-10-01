# forms.py
from django import forms

class ProductRatingForm(forms.Form):
    price_rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'step': '1'}),
        label='Precio'
    )
    quality_rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'step': '1'}),
        label='Calidad'
    )
    warranty_rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'step': '1'}),
        label='Garantía'
    )
    description = forms.CharField(max_length=500, label = "Descripción")
