from apps.books.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "description", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")
