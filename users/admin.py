from django.contrib import admin
from .models import  User, UserBilling
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name',
                    'last_name', 'is_superuser', 'is_staff', 'date_joined']
    exclude = ["username"]
    fieldsets = [
        (None,
         {
             'fields': ['password', 'stripe', 'last_login', 'date_joined']
        }
         ),
        ('Personal info',
         {
            'fields':
            [
            'first_name', 'last_name', 'email','subscription'
            ]
        }
         ),
        ('Permissions', {
            'fields': ['is_active', 'is_staff', 'is_superuser', 'user_permissions'],
        }),
    ]
    readonly_fields = ['date_joined', 'last_login', 'stripe', 'is_staff', 'is_superuser']
    ordering = ('email',)

@admin.register(UserBilling)
class UserBAdmin(admin.ModelAdmin):
    pass