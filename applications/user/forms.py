from django import forms
from .models import newclient

class SignupForm(forms.ModelForm):
    class Meta:
        model = newclient
        fields = ['EmailAdress', 'Name', 'LastName', 'BirthDate', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
