from apps.books.models import Author
from rest_framework import serializers


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "avatar")


class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "avatar", "about", "biography")
