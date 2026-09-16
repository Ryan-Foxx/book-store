from apps.books.models import Publisher
from rest_framework import serializers


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "avatar", "about", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")
