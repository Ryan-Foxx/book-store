from apps.books.api.v1.public.serializers.category_serializers import (
    CategoryDetailSerializer,
    CategoryListSerializer,
)
from apps.books.selectors.category_selectors import (
    get_public_category_detail_queryset,
    get_public_category_list_queryset,
)
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
class CategoryViewSet(ReadOnlyModelViewSet):

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        return CategoryDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return get_public_category_list_queryset()
        return get_public_category_detail_queryset()
