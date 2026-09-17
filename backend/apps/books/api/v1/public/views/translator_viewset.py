from apps.books.api.v1.public.filters.translator_filters import TranslatorFilter
from apps.books.api.v1.public.pagination.translator_pagination import (
    TranslatorPagination,
)
from apps.books.api.v1.public.serializers.translator_serializers import (
    TranslatorDetailSerializer,
    TranslatorListSerializer,
)
from apps.books.selectors.translator_selectors import (
    get_public_translator_detail_queryset,
    get_public_translator_list_queryset,
)
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
class TranslatorViewSet(ReadOnlyModelViewSet):
    pagination_class = TranslatorPagination
    filterset_class = TranslatorFilter

    def get_serializer_class(self):
        if self.action == "list":
            return TranslatorListSerializer
        return TranslatorDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return get_public_translator_list_queryset()
        return get_public_translator_detail_queryset()
