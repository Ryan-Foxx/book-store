from apps.books.api.v1.admin.pagination.translator_pagination import (
    TranslatorPagination,
)
from apps.books.api.v1.admin.serializers.translator_serializers import (
    TranslatorSerializer,
)
from apps.books.selectors.translator_selectors import get_admin_translator_queryset
from rest_framework.viewsets import ModelViewSet


class TranslatorViewSet(ModelViewSet):
    pagination_class = TranslatorPagination

    serializer_class = TranslatorSerializer
    queryset = get_admin_translator_queryset()
