from apps.books.models import Category
from django_filters.rest_framework import CharFilter, FilterSet


class CategoryFilter(FilterSet):

    # Search
    search = CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ()
