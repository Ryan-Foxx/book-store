from apps.books.api.v1.admin.filters.translator_filters import TranslatorFilter
from apps.books.api.v1.admin.pagination.translator_pagination import (
    TranslatorPagination,
)
from apps.books.api.v1.admin.permissions.translator_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.translator_serializers import (
    TranslatorSerializer,
)
from apps.books.selectors.translator_selectors import get_admin_translator_queryset
from core.permissions import IsOwner
from rest_framework.viewsets import ModelViewSet


class TranslatorViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = TranslatorPagination
    filterset_class = TranslatorFilter

    serializer_class = TranslatorSerializer
    queryset = get_admin_translator_queryset()
