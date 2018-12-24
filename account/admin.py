from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from account.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_faculty', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important date'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email', 'password'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
