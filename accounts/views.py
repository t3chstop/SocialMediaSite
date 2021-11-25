from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, UserSearchForm
from friendship.models import Friend  # type: ignore
from friendship.models import FriendshipRequest # type: ignore

# Create your views here.

#Home page when the site is first entered
def index(request):
	return render(request, 'accounts/index.html')

#Sign up page
def register(request):
	if request.user.is_authenticated:
		return redirect('/dashboard')
	#Recieve form information
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

#Login Page
def login(request):
	if request.user.is_authenticated:
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


@login_required
def dashboard(request):
	pending_friend_requests = Friend.objects.unrejected_requests(user=request.user)
	#I don't know how to do this without a form. Perhaps there is a better way with JS
	if request.method == 'POST':
		form = UserSearchForm(request.POST)
		if form.is_valid():
			user_entered_displayname = request.POST['display_name']
			return redirect(f'/profile/{user_entered_displayname}')
	else:
		form = UserSearchForm()
	return render(request, 'accounts/dashboard.html', {'form': form, 'pending_friend_requests':pending_friend_requests})