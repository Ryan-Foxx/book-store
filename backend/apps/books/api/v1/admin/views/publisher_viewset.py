from apps.books.api.v1.admin.serializers.publisher_serializers import (
    PublisherSerializer,
)
from apps.books.selectors.publisher_selectors import get_admin_publisher_queryset
from rest_framework.viewsets import ModelViewSet


class PublisherViewSet(ModelViewSet):
    serializer_class = PublisherSerializer
    queryset = get_admin_publisher_queryset()
