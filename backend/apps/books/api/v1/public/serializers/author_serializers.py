from apps.books.models import Author, Award
from rest_framework import serializers


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ("id", "title", "year_received")


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "avatar")


class AuthorDetailSerializer(serializers.ModelSerializer):
    awards = AwardSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ("id", "name", "avatar", "about", "biography", "awards")
