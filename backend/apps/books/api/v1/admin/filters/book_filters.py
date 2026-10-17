from apps.books.models import Book
from django.db.models import Q
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    OrderingFilter,
)


class BookFilter(FilterSet):

    # Boolean Filter
    is_active = BooleanFilter(field_name="is_active")

    # Search
    search = CharFilter(method="filter_search")

    # Ordering
    ordering = OrderingFilter(
        fields=(
            ("id", "id"),
            ("price", "price"),
            ("publication_date", "publication_date"),
            ("created_at", "created_at"),
            ("modified_at", "modified_at"),
        ),
        field_labels={
            "id": "id",
            "price": "price",
            "publication_date": "publication_date",
            "created_at": "created_at",
            "modified_at": "modified_at",
        },
    )

    class Meta:
        model = Book
        fields = ()

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(authors__name__icontains=value)).distinct()
