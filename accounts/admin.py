from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

#Custom Account Admin
class AccountAdmin(UserAdmin):
    list_display = ('email', 'displayName', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'displayName')
    readonly_fields = ('last_login', )

    filter_horizontal = ()
    filter_vertical = ()
    fieldsets = ()

    list_filter = ()

    ordering = ('last_login',)

admin.site.register(Account, AccountAdmin)