from django import forms
from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ["email", "first_name", "last_name", "username"]
    search_help_text = "Search by mail, username, first name and last name"
    exclude = ["password"]
    readonly_fields = ["last_login", "date_joined"]
