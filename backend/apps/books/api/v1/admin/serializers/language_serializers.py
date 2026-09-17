from apps.books.models import Language
from rest_framework import serializers


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("id", "name", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")
