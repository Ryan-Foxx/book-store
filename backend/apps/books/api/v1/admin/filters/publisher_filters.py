from apps.books.models import Publisher
from django_filters.rest_framework import CharFilter, FilterSet, OrderingFilter


class PublisherFilter(FilterSet):

    # Search
    search = CharFilter(field_name="name", lookup_expr="icontains")

    # Ordering
    ordering = OrderingFilter(
        fields=(
            ("id", "id"),
            ("created_at", "created_at"),
            ("modified_at", "modified_at"),
        ),
        field_labels={
            "id": "id",
            "created_at": "created_at",
            "modified_at": "modified_at",
        },
    )

    class Meta:
        model = Publisher
        fields = ()
