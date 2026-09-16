from apps.books.api.v1.admin.filters.category_filters import CategoryFilter
from apps.books.api.v1.admin.pagination.category_pagination import CategoryPagination
from apps.books.api.v1.admin.permissions.category_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.category_serializers import CategorySerializer
from apps.books.selectors.category_selectors import get_admin_category_queryset
from core.permissions import IsOwner
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = CategoryPagination
    filterset_class = CategoryFilter

    serializer_class = CategorySerializer
    queryset = get_admin_category_queryset()
