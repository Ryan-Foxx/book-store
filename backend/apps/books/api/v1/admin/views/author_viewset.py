from apps.books.api.v1.admin.pagination.author_pagination import AuthorPagination
from apps.books.api.v1.admin.serializers.author_serializers import AuthorSerializer
from apps.books.selectors.author_selectors import get_admin_author_queryset
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class AuthorViewSet(ModelViewSet):
    pagination_class = AuthorPagination

    serializer_class = AuthorSerializer
    queryset = get_admin_author_queryset()
