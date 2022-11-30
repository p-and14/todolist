from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user__username")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "created", "updated")
    search_fields = ("title", "description", "user__username")


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "updated", "goal")
    search_fields = ("text", "user__username", "goal__title")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
