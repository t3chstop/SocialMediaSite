from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from .models import Account

# Create your views here.

#Homepage
def Home_view(request):
	return render(request, 'accounts/home.html')

def Register_view(request):
	user=request.user
	if user.is_authenticated:
		return redirect('/dashboard')
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

def Login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect('/dashboard')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				return redirect('/dashboard')
		else:
			return HttpResponse("Login failed. Please try again")
	else:
		form = LoginForm()
		return render(request, 'accounts/login.html', {'form': form})


def Dashboard_view(request):
	return render(request, 'accounts/dashboard.html')

def Logout_view(request):
	logout(request)
	return redirect('/login')

