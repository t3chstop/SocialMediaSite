"""Social_Media_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import Friends
from accounts import views as Accountviews
from Friends import views as Friendviews

urlpatterns = [
    path('', Accountviews.Home_view, name="Home"),
    path('admin/', admin.site.urls),
    path('dashboard/', Accountviews.Dashboard_view, name="dashboard"),
    path('friendsearch/', Friendviews.friendsearch_view, name="Friendsearch"),
    path('logout/', Accountviews.Logout_view, name="Logout"),
    path('login/', Accountviews.Login_view, name="Login"),
    path('register/', Accountviews.Register_view, name="register"),
]