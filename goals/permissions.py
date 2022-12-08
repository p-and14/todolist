from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalCategoryCreatePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return BoardParticipant.objects.filter(
            user=request.user,
            board=request.data["board"],
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalCreatePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return BoardParticipant.objects.filter(
            user=request.user,
            board__categories__exact=request.data["category"],
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalCommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.goal.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalCommentCreatePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return BoardParticipant.objects.filter(
            user=request.user,
            board__categories__goals__exact=request.data["goal"],
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()
