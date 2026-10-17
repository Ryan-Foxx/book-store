from apps.books.api.v1.admin.pagination.book_pagination import BookPagination
from apps.books.api.v1.admin.serializers.book_serializers import (
    BookReadSerializer,
    BookSerializer,
)
from apps.books.selectors.book_selectors import get_admin_book_queryset
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class BookViewSet(ModelViewSet):
    pagination_class = BookPagination

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BookReadSerializer
        return BookSerializer

    queryset = get_admin_book_queryset()
