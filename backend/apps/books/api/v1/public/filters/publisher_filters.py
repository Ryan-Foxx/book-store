from apps.books.models import Publisher
from django_filters.rest_framework import CharFilter, FilterSet


class PublisherFilter(FilterSet):

    # Search
    search = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Publisher
        fields = ()
