from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter, GoalCommentFilter, GoalCategoryFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals import serializers
from goals import permissions
from goals.serializers import BoardCreateSerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated, permissions.GoalCategoryCreatePermissions]
    serializer_class = serializers.GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalCategoryFilter
    ordering_fields = ["title", "created", "id"]
    ordering = ["title", "id"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = serializers.GoalCategorySerializer
    permission_classes = [IsAuthenticated, permissions.GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        Goal.objects.filter(user=self.request.user, category=instance).update(status=Goal.Status.archived)

        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated, permissions.GoalCreatePermissions]
    serializer_class = serializers.GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["priority", "due_date", "id"]
    ordering = ["priority", "due_date", "id"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user, status__in=Goal.Status.values[:3])


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = serializers.GoalSerializer
    permission_classes = [IsAuthenticated, permissions.GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user, status__in=Goal.Status.values[:3])

    def perform_destroy(self, instance):
        instance.status = 4
        instance.save()
        return instance


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated, permissions.GoalCommentCreatePermissions]
    serializer_class = serializers.GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalCommentFilter
    ordering_fields = ["created", "updated", ]
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = serializers.GoalCommentSerializer
    permission_classes = [IsAuthenticated, permissions.GoalCommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user)


class BoardCreateView(generics.CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.BoardPermissions]
    serializer_class = serializers.BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related("participants").filter(
            participants__user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardListView(generics.ListAPIView):
    model = Board
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["title", "id"]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.prefetch_related("participants").filter(
            participants__user=self.request.user, is_deleted=False
        )
