from apps.books.models import Author, Book, Category, Publisher, Translator
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


class BookReadSerializer(serializers.ModelSerializer):
    # Related Fields
    authors = AuthorSerializer(many=True, read_only=True)
    translators = TranslatorSerializer(many=True, read_only=True)
    categories = CategorySerializer(source="category", many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    language = serializers.CharField(source="language.name", read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "avatar",
            "price",
            "number_of_pages",
            "publication_date",
            "language",
            "inventory",
            "is_active",
            "created_at",
            "modified_at",
            "authors",
            "translators",
            "categories",
            "publisher",
        )


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "avatar",
            "price",
            "number_of_pages",
            "publication_date",
            "authors",
            "translators",
            "category",
            "publisher",
            "language",
            "inventory",
            "is_active",
            "created_at",
            "modified_at",
        )
        read_only_fields = ("id", "created_at", "modified_at")
