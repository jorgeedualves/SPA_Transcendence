from django.contrib.auth.forms import UserCreationForm

from authentication.models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
