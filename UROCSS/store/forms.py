<<<<<<< HEAD

=======
>>>>>>> da6641f8e10f3dfcad6a229989def4f41845888e
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# from .models import CustomUser


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# class CustomUserChangeFrom(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ("username", "email")
