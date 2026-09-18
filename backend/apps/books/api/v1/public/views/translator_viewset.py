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
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all translators", tags=["Public - Translators"], auth=[]),
    retrieve=extend_schema(summary="Retrieve translator details", tags=["Public - Translators"], auth=[]),
)
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
