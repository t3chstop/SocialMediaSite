from django.contrib.auth.models import User
from accounts.forms import UserModel
from django import forms
from django.contrib.auth import get_user_model  

UserModel = get_user_model

class friendsearch_form(forms.Form):
    display_name = forms.CharField(max_length=300, help_text='Enter the display name of the user(caps sensitive)')
    context = {}

    class Meta:
        model = UserModel
        fields = ['display_name']