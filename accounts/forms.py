from django import forms
from django.contrib.auth.forms import UserCreationForm
from tempus_dominus.widgets import DatePicker
from bizz.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone',  'password1', 'password2')
