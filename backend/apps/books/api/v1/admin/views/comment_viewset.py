from apps.books.api.v1.admin.filters.comment_filters import CommentFilter
from apps.books.api.v1.admin.pagination.comment_pagination import CommentPagination
from apps.books.api.v1.admin.permissions.comment_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.comment_serializers import (
    CommentCreateSerializer,
    CommentReadSerializer,
)
from apps.books.selectors.comment_selectors import (
    get_admin_comment_list_queryset,
    get_admin_comment_queryset,
)
from core.permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all comments", tags=["Admin - Comments"]),
    create=extend_schema(summary="Create a new comment", tags=["Admin - Comments"]),
    retrieve=extend_schema(summary="Retrieve comment details", tags=["Admin - Comments"]),
    update=extend_schema(summary="Update an comment", tags=["Admin - Comments"]),
    partial_update=extend_schema(summary="Partially update an comment", tags=["Admin - Comments"]),
    destroy=extend_schema(summary="Delete an comment", tags=["Admin - Comments"]),
)
class CommentViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = CommentPagination
    filterset_class = CommentFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommentReadSerializer
        return CommentCreateSerializer

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return get_admin_comment_list_queryset()
        return get_admin_comment_queryset()
