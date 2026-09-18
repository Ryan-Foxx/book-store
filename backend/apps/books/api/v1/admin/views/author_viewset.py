from apps.books.api.v1.admin.filters.author_filters import AuthorFilter
from apps.books.api.v1.admin.pagination.author_pagination import AuthorPagination
from apps.books.api.v1.admin.permissions.author_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.author_serializers import AuthorSerializer
from apps.books.selectors.author_selectors import get_admin_author_queryset
from core.permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all authors", tags=["Admin - Authors"]),
    create=extend_schema(summary="Create a new author", tags=["Admin - Authors"]),
    retrieve=extend_schema(summary="Retrieve author details", tags=["Admin - Authors"]),
    update=extend_schema(summary="Update an author", tags=["Admin - Authors"]),
    partial_update=extend_schema(summary="Partially update an author", tags=["Admin - Authors"]),
    destroy=extend_schema(summary="Delete an author", tags=["Admin - Authors"]),
)
class AuthorViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = AuthorPagination
    filterset_class = AuthorFilter

    serializer_class = AuthorSerializer
    queryset = get_admin_author_queryset()
