from apps.books.models import Book
from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet, OrderingFilter


class BookFilter(FilterSet):

    # Search
    search = CharFilter(method="filter_search")

    # Ordering
    ordering = OrderingFilter(
        fields=(
            ("price", "price"),
            ("created_at", "created_at"),
        ),
        field_labels={
            "price": "price",
            "created_at": "created_at",
        },
    )

    class Meta:
        model = Book
        fields = ()

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(authors__name__icontains=value)).distinct()
