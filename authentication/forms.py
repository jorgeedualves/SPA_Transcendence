from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from authentication.models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    otp_token = forms.CharField(required=True, label='OTP Token')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        otp_token = cleaned_data.get('otp_token')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Invalid username or password')

        from django_otp import devices_for_user
        for device in devices_for_user(user):
            if device.verify_token(otp_token):
                return cleaned_data
        raise forms.ValidationError('Invalid OTP token')
