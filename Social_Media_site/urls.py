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
from accounts import views as accountViews
from chat import views as chatViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', accountViews.Home_view, name="Home"),
    path(r'admin/', admin.site.urls),
    path('dashboard/', accountViews.Dashboard_view, name="dashboard"),
    path('logout/', accountViews.Logout_view, name="Logout"),
    path('login/', accountViews.Login_view, name="Login"),
    path('register/', accountViews.Register_view, name="register"),
    path('setup/', accountViews.Setup_view, name="setup"),
    path('profile/<display_name>/', accountViews.Profile),
    path('chat/', include('chat.urls')),
    path('rooms/', chatViews.rooms),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
