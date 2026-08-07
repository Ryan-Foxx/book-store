from apps.books.models import Author
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "avatar", "about", "biography", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")
