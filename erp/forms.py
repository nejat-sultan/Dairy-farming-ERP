from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class PasswordInputWithPlaceholder(forms.PasswordInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', 'placeholder': 'Password'})

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInputWithPlaceholder)
    password2 = forms.CharField(widget=PasswordInputWithPlaceholder)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }