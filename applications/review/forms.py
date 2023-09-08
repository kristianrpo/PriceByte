from django import forms

class RatingForm(forms.Form):
    WARRANTY_CHOICES = (
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas'),
    )

    warranty_rating = forms.ChoiceField(choices=WARRANTY_CHOICES, label='Calificación de garantía', widget=forms.HiddenInput())
    price_rating = forms.ChoiceField(choices=WARRANTY_CHOICES, label='Calificación de precio', widget=forms.HiddenInput())
    quality_rating = forms.ChoiceField(choices=WARRANTY_CHOICES, label='Calificación de calidad', widget=forms.HiddenInput())
    overall_rating = forms.IntegerField(label='Calificación general')