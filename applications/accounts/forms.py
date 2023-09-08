from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

TYPE_CHOICES =(
    ("vendedor", "vendedor"),
    ("cliente", "cliente"),
)

class UserCreateForm(UserCreationForm):
    email = forms.CharField()
    #type = forms.CharField()
    type = forms.ChoiceField(choices = TYPE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        for fieldname in ['username', 'password1', 'password2', 'email']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                                      {'class': 'form-control'})
            
    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = ['username', 'email', 'type', 'password1', 'password2']

