from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for the User model.

    Role is the source of truth for permission flags, so `is_staff`
    and `is_superuser` are displayed as read-only fields.
    """

    model = User

    list_display = (
        "id",
        "username",
        "email",
        "phone_number",
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "last_login",
        "date_joined",
        "is_staff",
        "is_superuser",
    )

    ordering = ("-date_joined",)

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "first_name", "last_name", "phone_number", "role")}),
    )

    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("phone_number", "role")}),)
