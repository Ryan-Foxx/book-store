from apps.books.api.v1.public.serializers.book_serializers import (
    BookDetailSerializer,
    BookListSerializer,
)
from apps.books.models import Favorite
from apps.books.selectors.book_selectors import (
    get_public_book_detail_queryset,
    get_public_book_list_queryset,
)
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
class BookViewSet(ReadOnlyModelViewSet):

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return get_public_book_list_queryset()
        return get_public_book_detail_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user

        if user.is_authenticated:
            favorite_book_ids = set(Favorite.objects.filter(user=user).values_list("book_id", flat=True))
        else:
            favorite_book_ids = set()

        context["favorite_book_ids"] = favorite_book_ids
        return context
