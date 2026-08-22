from apps.books.models import Author, Award
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name")


class AwardReadSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Award
        fields = ("id", "authors", "title", "year_received", "created_at", "modified_at")


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ("id", "authors", "title", "year_received", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")
