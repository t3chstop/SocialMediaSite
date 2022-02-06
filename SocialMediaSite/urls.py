"""SocialMediaSite URL Configuration

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

"""
Planned URL Scheme:
domain.com - Show a welcome page that sells the site
domain.com/register/ - Sign up/registration page. Users create accounts here
domain.com/login/ - Login page.
domain.com/dashboard/ - Dashboard page
domain.com/profile/<user>/ - User profile
domain.com/edit-profile/ - Edit user profile
domain.com/logout/ - Logout(will contain template. just a redirect)
domain.com/chat/ - Page with all of users chatrooms
domain.com/chat/ws/key - Page with an active chatroom(ws indicates websocket connection)
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
