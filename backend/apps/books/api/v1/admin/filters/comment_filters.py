from apps.books.models import Comment
from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet, OrderingFilter


class CommentFilter(FilterSet):

    # Search
    search = CharFilter(method="filter_search")

    # Ordering
    ordering = OrderingFilter(
        fields=(
            ("id", "id"),
            ("created_at", "created_at"),
            ("modified_at", "modified_at"),
            ("user__username", "username"),
            ("book__name", "book"),
        ),
        field_labels={
            "id": "id",
            "created_at": "created_at",
            "modified_at": "modified_at",
            "user__username": "username",
            "book__name": "book",
        },
    )

    class Meta:
        model = Comment
        fields = ()

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(user__username__icontains=value) | Q(book__name__icontains=value)).distinct()
