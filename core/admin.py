from django import forms
from django.contrib import admin

from core.models import User


class UserForm(forms.ModelForm):
    new_password = forms.CharField()

    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ["email", "first_name", "last_name", "username"]
    search_help_text = "Search by mail, username, first name and last name"
    exclude = ["password"]
    readonly_fields = ["last_login", "date_joined"]

    def save_model(self, request, obj, form, change):
        if request.POST["new_password"]:
            password = request.POST["new_password"]
            obj.set_password(password)

        obj.save()
