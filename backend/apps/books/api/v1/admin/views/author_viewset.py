from apps.books.api.v1.admin.filters.author_filters import AuthorFilter
from apps.books.api.v1.admin.pagination.author_pagination import AuthorPagination
from apps.books.api.v1.admin.permissions.author_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.author_serializers import AuthorSerializer
from apps.books.selectors.author_selectors import get_admin_author_queryset
from core.permissions import IsOwner
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class AuthorViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = AuthorPagination
    filterset_class = AuthorFilter

    serializer_class = AuthorSerializer
    queryset = get_admin_author_queryset()
