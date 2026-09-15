from apps.books.models import Translator
from rest_framework import serializers


class TranslatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translator
        fields = ("id", "name", "avatar", "about", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")
