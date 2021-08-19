from django.core.exceptions import RequestAborted
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms import forms
from .forms import RegistrationForm, LoginForm, SetupForm, UserSearchForm
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
		form = RegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(email=email, password=raw_password)
			login(request, user)
			return redirect('/setup')
	else:
		form = RegistrationForm()
	
	return render(request, 'accounts/register.html', {'form': form})

def Setup_view(request):
	user = request.user
	if request.method == 'POST':
		form = SetupForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect('/dashboard')	
	else:
		form = SetupForm()
	return render(request, 'accounts/setup.html', {'form': form})

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
	user = request.user
	if request.method == 'POST':
		form = UserSearchForm(request.POST)
		if form.is_valid():
			user_entered_displayname = request.POST['display_name']
			return redirect(f'/profile/{user_entered_displayname}')
	else:
		form = UserSearchForm()
	return render(request, 'accounts/dashboard.html', {'form': form})

@login_required(login_url='/login/')
def Profile(request, display_name):
	requested_user = Account.objects.get(display_name=display_name)
	return render(request, 'accounts/profile.html', {"requested_user":requested_user})

def Logout_view(request):
	logout(request)
	return redirect('/login')