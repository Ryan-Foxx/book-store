from apps.books.api.v1.admin.filters.language_filters import LanguageFilter
from apps.books.api.v1.admin.pagination.language_pagination import LanguagePagination
from apps.books.api.v1.admin.permissions.language_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.language_serializers import LanguageSerializer
from apps.books.selectors.language_selectors import get_admin_language_queryset
from core.permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all languages", tags=["Admin - Languages"]),
    create=extend_schema(summary="Create a new language", tags=["Admin - Languages"]),
    retrieve=extend_schema(summary="Retrieve language details", tags=["Admin - Languages"]),
    update=extend_schema(summary="Update an language", tags=["Admin - Languages"]),
    partial_update=extend_schema(summary="Partially update an language", tags=["Admin - Languages"]),
    destroy=extend_schema(summary="Delete an language", tags=["Admin - Languages"]),
)
class LanguageViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = LanguagePagination
    filterset_class = LanguageFilter

    serializer_class = LanguageSerializer
    queryset = get_admin_language_queryset()
