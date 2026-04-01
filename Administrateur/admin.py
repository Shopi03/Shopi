# Administrateur/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "nom", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "nom")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "nom", "password", "profil", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nom", "password1", "password2", "role", "profil", "is_staff", "is_active"),
        }),
    )

admin.site.register(User, UserAdmin)