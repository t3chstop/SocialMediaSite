from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, UserSearchForm
from friendship.models import Friend, FriendshipRequest  # type: ignore
from .models import Account
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
				django_login(request, user)
				return redirect('/dashboard')
		else:
			return HttpResponse("Login failed. Please try again")
	else:
		form = LoginForm()
		return render(request, 'accounts/login.html', {'form': form})

#Dashboard Page(home for logged in users)
@login_required
def dashboard(request):
	pending_friend_requests = Friend.objects.unrejected_requests(user=request.user)
	displayName = request.user.displayName
	#I don't know how to do this without a form. Perhaps there is a better way with JS
	if request.method == 'POST':
		form = UserSearchForm(request.POST)
		if form.is_valid():
			user_entered_displayname = request.POST['displayName']
			return redirect(f'/profile/{user_entered_displayname}')
	else:
		form = UserSearchForm()
	return render(request, 'accounts/dashboard.html', {'form': form, 'pending_friend_requests':pending_friend_requests, 'displayName':displayName})

#Logout view, just logs user out and redirects
def logout(request):
	django_logout(request) #New name to prevent recursion
	return redirect('/login')

#Profile view
def profile(request, displayName):
	"""
	This view must handle a few different situations.
	- If the person that is being viewed isn't a friend, allow them to
	send a friend request
	- If the person that is being viewed is a friend, allow them to remove
	the friendship
	- If viewing oneself, allow the user to edit their profile
	"""

	activeRequestTo = False
	activeRequestFrom = False
	areFriends = False
	viewingSelf = False

	try:
		displayed_user = Account.objects.get(displayName=displayName)
	except:
		return HttpResponse("404. User not found")


	if request.user==displayed_user:
		viewingSelf = True
		return render(request, 'accounts/profile.html', 
		{
			'viewingName' : request.user.displayName,
			'areFriends' : areFriends, 
			'activeRequestTo' : activeRequestTo, 
			'activeRequestFrom':activeRequestFrom,
			'viewingSelf' : viewingSelf,
		})

	#Check if user is friends already

	areFriends = Friend.objects.are_friends(request.user, displayed_user)

	try:
		activeRequestTo = FriendshipRequest.objects.get(to_user=request.user, from_user=displayed_user).exists()
	except:
		return render(request, 'accounts/profile.html', 
		{
			'viewingName' : displayed_user.displayName,
			'areFriends' : areFriends, 
			'activeRequestTo' : activeRequestTo, 
			'activeRequestFrom':activeRequestFrom,
			'viewingSelf' : viewingSelf,
		})

	try:
		activeRequestFrom = FriendshipRequest.objects.get(to_user=displayed_user, from_user=request.user).exists()
	except:
		pass

	return render(request, 'accounts/profile.html', 
		{
			'viewingName' : displayed_user.displayName,
			'areFriends' : areFriends, 
			'activeRequestTo' : activeRequestTo, 
			'activeRequestFrom':activeRequestFrom,
			'viewingSelf' : viewingSelf,
		})

