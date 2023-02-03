from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Register custom user model on admin site."""
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'tg_id')}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                     'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'last_name', 'first_name', 'password1',
                           'password2', 'email', 'tg_id')}),
    )
    list_display = ('id', 'username', 'last_name', 'first_name', 'email',
                    'tg_id', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')
