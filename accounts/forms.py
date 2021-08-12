from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import fields
from .models import Account
from django.contrib.auth import get_user_model  
from django.core.files.images import get_image_dimensions

UserModel = get_user_model()  
class RegistrationForm(UserCreationForm):
    context = {}
    email = forms.EmailField(max_length=255, help_text="You will log in with this")
    display_name = forms.CharField(max_length=300, help_text="This is how your friends will find you")
    profile_picture = forms.ImageField()
    

    class Meta:
        model = UserModel
        fields = ('email', 'display_name', 'profile_picture', 'password1', 'password2')

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data['profile_picture']

        try:
            w, h = get_image_dimensions(profile_picture)
            """
            #validate dimensions
            max_width = max_height = 360
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = profile_picture.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(profile_picture) > (50 * 1024):
                raise forms.ValidationError(
                    u'profile_picture file size may not exceed 20k.')
            """
        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new profile_picture
            """
            pass

        return profile_picture

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
