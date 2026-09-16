from apps.books.api.v1.admin.pagination.publisher_pagination import PublisherPagination
from apps.books.api.v1.admin.serializers.publisher_serializers import (
    PublisherSerializer,
)
from apps.books.selectors.publisher_selectors import get_admin_publisher_queryset
from rest_framework.viewsets import ModelViewSet


class PublisherViewSet(ModelViewSet):
    pagination_class = PublisherPagination

    serializer_class = PublisherSerializer
    queryset = get_admin_publisher_queryset()
