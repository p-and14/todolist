from django.contrib import admin

from goals.models import GoalCategory, Goal


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user__username")


class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "status",
        "created",
        "updated"
    )
    search_fields = ("title", "description", "user__username")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
