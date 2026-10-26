from apps.books.models import Book, Comment
from rest_framework import serializers
from rest_framework.exceptions import NotFound


class CommentListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    avatar = serializers.ImageField(source="user.profile.avatar", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "username", "avatar", "body", "created_at")


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "body")
        read_only_fields = ("id",)

    def validate(self, attrs):
        book_pk = self.context.get("book_pk")

        try:
            book_id = int(book_pk)
        except (TypeError, ValueError):
            raise serializers.ValidationError({"book_id": "Book ID must be a valid integer."})

        try:
            book = Book.objects.get(pk=book_id, is_active=True)
        except Book.DoesNotExist:
            raise NotFound(detail="Book not found.")

        attrs["book"] = book
        return attrs
