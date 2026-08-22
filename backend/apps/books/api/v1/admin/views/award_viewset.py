from apps.books.api.v1.admin.filters.award_filters import AwardFilter
from apps.books.api.v1.admin.pagination.award_pagination import AwardPagination
from apps.books.api.v1.admin.permissions.award_permissions import IsAdmin
from apps.books.api.v1.admin.serializers.award_serializers import (
    AwardReadSerializer,
    AwardSerializer,
)
from apps.books.selectors.award_selectors import get_admin_award_queryset
from core.permissions import IsOwner
from rest_framework.viewsets import ModelViewSet


class AwardViewSet(ModelViewSet):
    permission_classes = [IsOwner | IsAdmin]
    pagination_class = AwardPagination
    filterset_class = AwardFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AwardReadSerializer
        return AwardSerializer

    queryset = get_admin_award_queryset()
