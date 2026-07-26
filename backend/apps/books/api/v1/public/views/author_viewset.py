from apps.books.api.v1.public.pagination.author_pagination import AuthorPagination
from apps.books.api.v1.public.serializers.author_serializers import (
    AuthorDetailSerializer,
    AuthorListSerializer,
)
from apps.books.selectors.author_selectors import (
    get_public_author_detail_queryset,
    get_public_author_list_queryset,
)
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
class AuthorViewSet(ReadOnlyModelViewSet):
    pagination_class = AuthorPagination

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        return AuthorDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return get_public_author_list_queryset()
        return get_public_author_detail_queryset()
