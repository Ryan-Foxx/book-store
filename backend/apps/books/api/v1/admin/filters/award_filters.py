from apps.books.models import Award
from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet, OrderingFilter


class AwardFilter(FilterSet):

    # Search
    search = CharFilter(method="filter_search")

    # Ordering
    ordering = OrderingFilter(
        fields=(
            ("id", "id"),
            ("year_received", "year_received"),
            ("created_at", "created_at"),
            ("modified_at", "modified_at"),
        ),
        field_labels={
            "id": "id",
            "year_received": "year_received",
            "created_at": "created_at",
            "modified_at": "modified_at",
        },
    )

    class Meta:
        model = Award
        fields = ()

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(authors__name__icontains=value)).distinct()
