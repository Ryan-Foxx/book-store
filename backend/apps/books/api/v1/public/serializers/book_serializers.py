from apps.books.models import (
    Author,
    Book,
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


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("name",)


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "name", "avatar", "price")


class BookDetailSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    translators = TranslatorSerializer(many=True, read_only=True)
    categories = CategorySerializer(source="category", many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)

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
            "authors",
            "translators",
            "categories",
            "publisher",
            "language",
        )
