from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "board", "user", "created", "updated")
    search_fields = ("title", "user__username")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "created", "updated")
    search_fields = ("title", "description", "user__username")


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created", "updated", "goal")
    search_fields = ("text", "user__username", "goal__title")


class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "participants", "created", "updated", )
    search_fields = ("title", )

    def participants(self, obj):
        p = [row.user.username for row in BoardParticipant.objects.filter(board_id=obj.pk)]
        return p


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "board", "user", "created", "updated", )
    search_fields = ("title", )


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
