from django.contrib.auth.models import User
from accounts.models import Account
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'display_name', 'time_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'display_name')
    readonly_fields = ('id', 'time_joined', 'last_login')

    filter_horizontal = ()
    filter_vertical = ()
    fieldsets = ()

    list_filter = ()

    ordering = ()

admin.site.register(Account, AccountAdmin)