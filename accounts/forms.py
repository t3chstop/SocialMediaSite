from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import fields
from .models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='You will log in with this')
    display_name = forms.CharField(max_length=300, help_text='This is how your friends will find you')
    class Meta:
        model = Account
        fields = ['email', 'display_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is already linked to an account.')

    def display_name(self):
        display_name = self.cleaned_data['display_name']
        try:
            account = Account.objects.get(display_name=display_name)
        except Exception as e:
            return display_name
        raise forms.ValidationError(f'Display name {display_name} is already in use')