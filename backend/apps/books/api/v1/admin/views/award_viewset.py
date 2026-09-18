from apps.books.api.v1.admin.filters.award_filters import AwardFilter
from apps.books.api.v1.admin.pagination.award_pagination import AwardPagination
from apps.books.api.v1.admin.permissions.award_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.award_serializers import (
    AwardReadSerializer,
    AwardSerializer,
)
from apps.books.selectors.award_selectors import get_admin_award_queryset
from core.permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet


# Create your views here.
@extend_schema_view(
    list=extend_schema(summary="List all awards", tags=["Admin - Awards"]),
    create=extend_schema(summary="Create a new award", tags=["Admin - Awards"]),
    retrieve=extend_schema(summary="Retrieve award details", tags=["Admin - Awards"]),
    update=extend_schema(summary="Update an award", tags=["Admin - Awards"]),
    partial_update=extend_schema(summary="Partially update an award", tags=["Admin - Awards"]),
    destroy=extend_schema(summary="Delete an award", tags=["Admin - Awards"]),
)
class AwardViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = AwardPagination
    filterset_class = AwardFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AwardReadSerializer
        return AwardSerializer

    queryset = get_admin_award_queryset()
