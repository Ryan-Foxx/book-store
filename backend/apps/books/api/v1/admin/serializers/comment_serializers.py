from apps.books.models import Book, Comment
from rest_framework import serializers
from rest_framework.exceptions import NotFound


class CommentReadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    avatar = serializers.ImageField(source="user.profile.avatar", read_only=True)
    book = serializers.CharField(source="book.name", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "username", "avatar", "book", "body", "status", "created_at", "modified_at")


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "user", "book", "body", "status", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")
