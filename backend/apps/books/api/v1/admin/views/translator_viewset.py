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
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all translators", tags=["Admin - Translators"]),
    create=extend_schema(summary="Create a new translator", tags=["Admin - Translators"]),
    retrieve=extend_schema(summary="Retrieve translator details", tags=["Admin - Translators"]),
    update=extend_schema(summary="Update an translator", tags=["Admin - Translators"]),
    partial_update=extend_schema(summary="Partially update an translator", tags=["Admin - Translators"]),
    destroy=extend_schema(summary="Delete an translator", tags=["Admin - Translators"]),
)
class TranslatorViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = TranslatorPagination
    filterset_class = TranslatorFilter

    serializer_class = TranslatorSerializer
    queryset = get_admin_translator_queryset()
