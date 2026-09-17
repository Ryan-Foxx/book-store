from apps.books.api.v1.admin.filters.language_filters import LanguageFilter
from apps.books.api.v1.admin.pagination.language_pagination import LanguagePagination
from apps.books.api.v1.admin.permissions.language_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.language_serializers import LanguageSerializer
from apps.books.selectors.language_selectors import get_admin_language_queryset
from core.permissions import IsOwner
from rest_framework.viewsets import ModelViewSet


class LanguageViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = LanguagePagination
    filterset_class = LanguageFilter

    serializer_class = LanguageSerializer
    queryset = get_admin_language_queryset()
