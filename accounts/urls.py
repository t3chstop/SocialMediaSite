"""
Planned URL Scheme:
domain.com - Show a welcome page that sells the site
domain.com/register/ - Sign up/registration page. Users create accounts here
domain.com/login/ - Login page.
domain.com/dashboard/ - Dashboard page
domain.com/profile/<user>/ - User profile
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]