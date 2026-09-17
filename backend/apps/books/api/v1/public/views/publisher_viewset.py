from apps.books.api.v1.public.pagination.publisher_pagination import PublisherPagination
from apps.books.api.v1.public.serializers.publisher_serializers import (
    PublisherDetailSerializer,
    PublisherListSerializer,
)
from apps.books.selectors.publisher_selectors import (
    get_public_publisher_detail_queryset,
    get_public_publisher_list_queryset,
)
from rest_framework.viewsets import ReadOnlyModelViewSet


# Create your views here.
class PublisherViewSet(ReadOnlyModelViewSet):
    pagination_class = PublisherPagination

    def get_serializer_class(self):
        if self.action == "list":
            return PublisherListSerializer
        return PublisherDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return get_public_publisher_list_queryset()
        return get_public_publisher_detail_queryset()
