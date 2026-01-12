from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from .models import CustomUser

User = get_user_model()


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

class ProfileUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-0 bg-transparent shadow-none', 
            'placeholder': '*************'  
        }),
        required=False,
        label="New Password"
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "avatar"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control border-0 bg-transparent shadow-none'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control border-0 bg-transparent shadow-none'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-0 bg-transparent shadow-none'}),
        }