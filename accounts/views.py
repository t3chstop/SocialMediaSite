from typing import ContextManager
from accounts.models import Account
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, SignUpForm

def Home(request):
    return render(request, 'accounts/home.html')

def Register(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}")
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            authenticate(email=email, password=raw_password)
            login(request, Account)
            return redirect('/')

        else:
            context['registration_form'] = form

def sign_up(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        return HttpResponse(f'the method is {request.method}')
    return render(request, 'accounts/register.html', context)
