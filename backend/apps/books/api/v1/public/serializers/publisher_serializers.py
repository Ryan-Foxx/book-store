from apps.books.models import Publisher
from rest_framework import serializers


class PublisherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "avatar")


class PublisherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "avatar", "about")
