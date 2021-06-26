from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import fields
from .models import Account
from django.contrib.auth import get_user_model  

UserModel = get_user_model()  

class RegistrationForm(UserCreationForm):
	context = {}
	email = forms.EmailField(max_length=255, help_text="You will log in with this")
	display_name = forms.CharField(max_length=300, help_text="This is how your friends will find you")
	

	class Meta:
		model = UserModel
		fields = ('email', 'display_name','password1', 'password2')



