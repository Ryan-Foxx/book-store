from apps.books.models import Author
from django_filters.rest_framework import CharFilter, FilterSet


class AuthorFilter(FilterSet):
    
    # Search
    search = CharFilter(field_name="name", lookup_expr="icontains")
    
    class Meta:
        model = Author
        fields = ()
