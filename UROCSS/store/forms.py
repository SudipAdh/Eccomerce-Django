from django.forms import ModelForm
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User
from django import forms

# from .models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# class CustomUserChangeFrom(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ("username", "email")
