from apps.books.api.v1.admin.filters.publisher_filters import PublisherFilter
from apps.books.api.v1.admin.pagination.publisher_pagination import PublisherPagination
from apps.books.api.v1.admin.permissions.publisher_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.publisher_serializers import (
    PublisherSerializer,
)
from apps.books.selectors.publisher_selectors import get_admin_publisher_queryset
from core.permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all publishers", tags=["Admin - Publisher"]),
    create=extend_schema(summary="Create a new publisher", tags=["Admin - Publisher"]),
    retrieve=extend_schema(summary="Retrieve publisher details", tags=["Admin - Publisher"]),
    update=extend_schema(summary="Update an publisher", tags=["Admin - Publisher"]),
    partial_update=extend_schema(summary="Partially update an publisher", tags=["Admin - Publisher"]),
    destroy=extend_schema(summary="Delete an publisher", tags=["Admin - Publisher"]),
)
class PublisherViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = PublisherPagination
    filterset_class = PublisherFilter

    serializer_class = PublisherSerializer
    queryset = get_admin_publisher_queryset()
