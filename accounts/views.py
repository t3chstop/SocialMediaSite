from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return render(request, 'accounts/dashboard.html')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def dashboard(request):
    return render(request, 'dashboard.html')

def signout(request):
    logout(request)
    return redirect('/accounts/login')