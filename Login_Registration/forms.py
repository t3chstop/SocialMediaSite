from django import forms
from django.forms import ModelForm
from .models import customuser

class SignUpForm(ModelForm):
    class Meta:
        model = customuser
        fields = ['email', 'first_name', 'last_name', 'password']