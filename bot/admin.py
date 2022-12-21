from django.contrib import admin

from bot.models import TgUser


class TgUserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_user_id", "user")
    search_fields = ("telegram_user_id", "user__username")


admin.site.register(TgUser, TgUserAdmin)
