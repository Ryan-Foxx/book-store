from apps.books.api.v1.admin.serializers.category_serializers import CategorySerializer
from apps.books.selectors.category_selectors import get_admin_category_queryset
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = get_admin_category_queryset()
