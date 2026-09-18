from apps.books.api.v1.public.filters.author_filters import AuthorFilter
from apps.books.api.v1.public.pagination.author_pagination import AuthorPagination
from apps.books.api.v1.public.serializers.author_serializers import (
    AuthorDetailSerializer,
    AuthorListSerializer,
)
from apps.books.selectors.author_selectors import (
    get_public_author_detail_queryset,
    get_public_author_list_queryset,
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all authors", tags=["Public - Authors"], auth=[]),
    retrieve=extend_schema(summary="Retrieve author details", tags=["Public - Authors"], auth=[]),
)
class AuthorViewSet(ReadOnlyModelViewSet):
    pagination_class = AuthorPagination
    filterset_class = AuthorFilter

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        return AuthorDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return get_public_author_list_queryset()
        return get_public_author_detail_queryset()
