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
from accounts.models import Account
from django.contrib import admin
from django.urls import path, include
from accounts import views as Account_views
from Friends import views as Friends_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Account_views.Home_view, name="Home"),
    path('admin/', admin.site.urls),
    path('dashboard/', Account_views.Dashboard_view, name="dashboard"),
    path('logout/', Account_views.Logout_view, name="Logout"),
    path('login/', Account_views.Login_view, name="Login"),
    path('register/', Account_views.Register_view, name="register"),
    path('setup/', Account_views.Setup_view, name="setup"),
    path('friendship/', include('friendship.urls')),
    path('profile/<display_name>/', Account_views.Profile),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)