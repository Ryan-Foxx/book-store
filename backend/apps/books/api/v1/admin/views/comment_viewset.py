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
from rest_framework.viewsets import ModelViewSet


# Create your views here.
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
