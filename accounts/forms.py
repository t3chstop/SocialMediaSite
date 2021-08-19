from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db import models
from django.forms import fields
from .models import Account
from django.contrib.auth import get_user_model
from PIL import Image
import os, sys

UserModel = get_user_model()  
class RegistrationForm(UserCreationForm):
    context = {}
    email = forms.EmailField(max_length=255, help_text="You will log in with this")
    display_name = forms.CharField(max_length=300, help_text="This is how your friends will find you")
    

    class Meta:
        model = UserModel
        fields = ('email', 'display_name', 'password1', 'password2')

class SetupForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(max_length=700, required=False)
    

    class Meta:
        model = UserModel
        fields = ('profile_picture', 'bio')

class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Login Credentials not found")

class UserSearchForm(forms.Form):
    display_name = forms.CharField(label='Display Name')

    class Meta:
        model = Account
        fields = ('display_name')

    def clean(self):
        entered_display_name = self.cleaned_data['display_name']
        try:
            Account.objects.get(display_name=entered_display_name)
        except:
            raise forms.ValidationError("User not found.")