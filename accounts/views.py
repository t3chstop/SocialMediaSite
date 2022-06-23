from email import message
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, UserSearchForm, SetupForm, EditProfileForm
from friendship.models import Friend, FriendshipRequest, Block  # type: ignore
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
			django_login(request, user)
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
	requestNames = []
	for i in pending_friend_requests:
		requestNames.append(i.from_user.displayName)
	
	displayName = request.user.displayName
	#I don't know how to do this without a form. Perhaps there is a better way with JS
	if request.method == 'POST':
		form = UserSearchForm(request.POST)
		if form.is_valid():
			user_entered_displayname = request.POST['displayName']
			return redirect(f'/profile/{user_entered_displayname}')
	else:
		form = UserSearchForm()
	return render(request, 'accounts/dashboard.html', {'form': form, 'requestNames':requestNames, 'displayName':displayName})

#Setup page(One time after registration)
def setup(request):
	if request.method == 'POST':
		form = SetupForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('/dashboard')	
	else:
		form = SetupForm()
	return render(request, 'accounts/setup.html', {'form': form})

#Logout view, just logs user out and redirects
def logout(request):
	django_logout(request) #New name to prevent recursion
	return redirect('/login')

#Page where logged in user edits their profile
def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=request.user)
		form.actual_user = request.user
		if form.is_valid():
			if not form.data['displayName']:
				form.data['displayName'] = request.user.displayName
			if not form.data['email']:
				form.data['email'] = request.user.email
			if not form.data['bio']:
				form.data['bio'] = request.user.bio
			print(form.data)
			form.save()
			return redirect('/dashboard')
	else:
		form = EditProfileForm()
		form.fields['displayName'].widget.attrs['placeholder']=request.user.displayName
		form.fields['email'].widget.attrs['placeholder']=request.user.email
		form.fields['bio'].widget.attrs['placeholder']=request.user.bio
	return render(request, 'accounts/edit-profile.html', {'form': form,})

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

	
	if 'send_request_form' in request.POST:
		#Check if request.user is blocked by other user
		if Block.objects.is_blocked(request.user, displayed_user):
			return HttpResponse("this person has blocked you")
		Friend.objects.add_friend(request.user, displayed_user, message=request.POST["send_request_form_text"])
		return redirect('/dashboard')

	if 'accept_friend_form' in request.POST:
		friend_request = FriendshipRequest.objects.get(from_user=displayed_user, to_user=request.user)
		friend_request.accept() 

	if 'reject_friend_form' in request.POST:
		friend_request = FriendshipRequest.objects.get(from_user=displayed_user, to_user=request.user)
		friend_request.reject()

	if 'remove_friends_form' in request.POST:
		Friend.objects.remove_friend(request.user, displayed_user)
	
	if 'block_form' in request.POST:
		Block.objects.add_block(request.user, displayed_user)

	if 'unblock_form' in request.POST:
		Block.objects.remove_block(request.user, displayed_user)


	if request.user==displayed_user:
		viewingSelf = True
		return render(request, 'accounts/profile.html', 
		{
			'displayed_user' : displayed_user,
			'viewingName' : request.user.displayName,
			'areFriends' : areFriends, 
			'activeRequestTo' : activeRequestTo, 
			'activeRequestFrom':activeRequestFrom,
			'viewingSelf' : viewingSelf,
		})

	#Check if user is friends already

	areFriends = Friend.objects.are_friends(request.user, displayed_user)

	try:
		placeholder = FriendshipRequest.objects.get(to_user=request.user, from_user=displayed_user)
		activeRequestTo = True
		return render(request, 'accounts/profile.html', 
				{
					'viewingName' : displayed_user.displayName,
					'areFriends' : areFriends, 
					'activeRequestTo' : activeRequestTo, 
					'activeRequestFrom':activeRequestFrom,
					'viewingSelf' : viewingSelf,
				})
	except:
		pass
		

	try:
		placeholder = FriendshipRequest.objects.get(to_user=displayed_user, from_user=request.user)
		activeRequestFrom = True
		return render(request, 'accounts/profile.html', 
		{
			'viewingName' : displayed_user.displayName,
			'areFriends' : areFriends, 
			'activeRequestTo' : activeRequestTo, 
			'activeRequestFrom':activeRequestFrom,
			'viewingSelf' : viewingSelf,
		})
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



