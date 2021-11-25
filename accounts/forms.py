from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

#Get the user model
UserModel = get_user_model()

class RegistrationForm(UserCreationForm):
    context = {}
    email = forms.EmailField(max_length=255, help_text="You will log in with this")
    displayName = forms.CharField(max_length=300, help_text="This name will appear with your public profile")
    

    class Meta:
        model = UserModel
        fields = ('email', 'displayName', 'password1', 'password2')

class SetupForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(max_length=700, required=False)
    

    class Meta:
        model = UserModel
        fields = ('profile_picture', 'bio')