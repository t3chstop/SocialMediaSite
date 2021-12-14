from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate

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


class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        if self.is_valid:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Login Credentials not found")

class UserSearchForm(forms.Form):
    displayName = forms.CharField(max_length=30)

    def clean(self):
        entered_display_name = self.data['displayName']
        try:
            UserModel.objects.get(display_name=entered_display_name)
        except:
            raise forms.ValidationError("User not found")