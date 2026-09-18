from apps.books.api.v1.admin.filters.category_filters import CategoryFilter
from apps.books.api.v1.admin.pagination.category_pagination import CategoryPagination
from apps.books.api.v1.admin.permissions.category_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.category_serializers import CategorySerializer
from apps.books.selectors.category_selectors import get_admin_category_queryset
from core.permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all categories", tags=["Admin - Categories"]),
    create=extend_schema(summary="Create a new category", tags=["Admin - Categories"]),
    retrieve=extend_schema(summary="Retrieve category details", tags=["Admin - Categories"]),
    update=extend_schema(summary="Update an category", tags=["Admin - Categories"]),
    partial_update=extend_schema(summary="Partially update an category", tags=["Admin - Categories"]),
    destroy=extend_schema(summary="Delete an category", tags=["Admin - Categories"]),
)
class CategoryViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = CategoryPagination
    filterset_class = CategoryFilter

    serializer_class = CategorySerializer
    queryset = get_admin_category_queryset()
