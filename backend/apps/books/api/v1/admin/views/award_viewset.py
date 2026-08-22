from apps.books.api.v1.admin.serializers.award_serializers import (
    AwardReadSerializer,
    AwardSerializer,
)
from apps.books.selectors.award_selectors import get_admin_award_queryset
from rest_framework.viewsets import ModelViewSet


class AwardViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AwardReadSerializer
        return AwardSerializer

    queryset = get_admin_award_queryset()
