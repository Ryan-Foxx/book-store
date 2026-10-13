from apps.books.models import (
    Author,
    Book,
    BookDetail,
    Category,
    Language,
    Publisher,
    Translator,
)
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name")


class TranslatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translator
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name")


class BookMoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetail
        fields = ("id", "order", "section_type", "text", "image")


class BookListSerializer(serializers.ModelSerializer):
    # Related Fields
    language = serializers.CharField(source="language.name", read_only=True)

    # Annotate Fields
    rating_average = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = ("id", "name", "avatar", "price", "language", "rating_average")


class BookDetailSerializer(serializers.ModelSerializer):
    # Related Fields
    authors = AuthorSerializer(many=True, read_only=True)
    translators = TranslatorSerializer(many=True, read_only=True)
    categories = CategorySerializer(source="category", many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    language = serializers.CharField(source="language.name", read_only=True)
    details = BookMoreDetailSerializer(many=True, read_only=True)

    # Custom Method Fields
    is_favorited = serializers.SerializerMethodField()

    # Annotate Fields
    rating_average = serializers.FloatField(read_only=True)
    ratings_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "avatar",
            "price",
            "number_of_pages",
            "publication_date",
            "inventory",
            "is_favorited",
            "rating_average",
            "ratings_count",
            "details",
            "authors",
            "translators",
            "categories",
            "publisher",
            "language",
        )

    def get_is_favorited(self, book: Book):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        favorite_book_ids = self.context.get("favorite_book_ids", set())
        return book.id in favorite_book_ids
