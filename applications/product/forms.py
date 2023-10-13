from django import forms

class form_favorite(forms.ModelForm):
    class Meta:
        fields = (
            'user',
            'product',
        )
        