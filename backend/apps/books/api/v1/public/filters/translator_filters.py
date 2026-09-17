from apps.books.models import Translator
from django_filters.rest_framework import CharFilter, FilterSet


class TranslatorFilter(FilterSet):

    # Search
    search = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Translator
        fields = ()
