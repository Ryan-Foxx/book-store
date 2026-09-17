from apps.books.api.v1.admin.serializers.language_serializers import LanguageSerializer
from apps.books.selectors.language_selectors import get_admin_language_queryset
from rest_framework.viewsets import ModelViewSet


class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    queryset = get_admin_language_queryset()
