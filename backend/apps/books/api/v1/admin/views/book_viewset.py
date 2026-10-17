from apps.books.api.v1.admin.filters.book_filters import BookFilter
from apps.books.api.v1.admin.pagination.book_pagination import BookPagination
from apps.books.api.v1.admin.permissions.book_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.book_serializers import (
    BookReadSerializer,
    BookSerializer,
)
from apps.books.selectors.book_selectors import get_admin_book_queryset
from core.permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all books", tags=["Admin - Books"]),
    create=extend_schema(summary="Create a new book", tags=["Admin - Books"]),
    retrieve=extend_schema(summary="Retrieve book details", tags=["Admin - Books"]),
    update=extend_schema(summary="Update an book", tags=["Admin - Books"]),
    partial_update=extend_schema(summary="Partially update an book", tags=["Admin - Books"]),
    destroy=extend_schema(summary="Delete an book", tags=["Admin - Books"]),
)
class BookViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = BookPagination
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BookReadSerializer
        return BookSerializer

    queryset = get_admin_book_queryset()
