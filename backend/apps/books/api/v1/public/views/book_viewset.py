from apps.books.api.v1.public.pagination.book_pagination import BookPagination
from apps.books.api.v1.public.serializers.book_serializers import (
    BookDetailSerializer,
    BookListSerializer,
)
from apps.books.selectors.book_selectors import (
    get_public_book_detail_queryset,
    get_public_book_list_queryset,
)
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
class BookViewSet(ReadOnlyModelViewSet):
    pagination_class = BookPagination

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return get_public_book_list_queryset()
        return get_public_book_detail_queryset(user=self.request.user)
