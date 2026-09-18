from apps.books.api.v1.public.filters.category_filters import CategoryFilter
from apps.books.api.v1.public.pagination.category_pagination import (
    CategoryPagination,
)
from apps.books.api.v1.public.serializers.category_serializers import (
    CategoryDetailSerializer,
    CategoryListSerializer,
)
from apps.books.selectors.category_selectors import (
    get_public_category_detail_queryset,
    get_public_category_list_queryset,
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all categories", tags=["Public - Categories"], auth=[]),
    retrieve=extend_schema(summary="Retrieve category details", tags=["Public - Categories"], auth=[]),
)
class CategoryViewSet(ReadOnlyModelViewSet):
    pagination_class = CategoryPagination
    filterset_class = CategoryFilter

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        return CategoryDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return get_public_category_list_queryset()
        return get_public_category_detail_queryset()
