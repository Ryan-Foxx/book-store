from apps.books.models import (
    Author,
    Award,
    Book,
    Category,
    Language,
    Publisher,
    Translator,
)
from django.contrib import admin


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author

    list_display = (
        "id",
        "name",
        "avatar",
        "about",
        "biography",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "created_at",
        "modified_at",
    )

    list_per_page = 10
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    model = Award

    list_display = (
        "id",
        # "authors",
        "title",
        "year_received",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "created_at",
        "modified_at",
    )

    list_per_page = 10
    search_fields = ("title",)
    ordering = ("-created_at",)
    filter_horizontal = ("authors",)


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    model = Translator

    list_display = (
        "id",
        "name",
        "avatar",
        "about",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "created_at",
        "modified_at",
    )

    list_per_page = 10
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    model = Publisher

    list_display = (
        "id",
        "name",
        "avatar",
        "about",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "created_at",
        "modified_at",
    )

    list_per_page = 10
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = (
        "id",
        "title",
        "description",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "created_at",
        "modified_at",
    )

    list_per_page = 10
    search_fields = ("title",)
    ordering = ("-created_at",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    model = Language

    list_display = (
        "id",
        "name",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "created_at",
        "modified_at",
    )

    list_per_page = 10
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    model = Book

    list_display = (
        "id",
        "name",
        "avatar",
        "price",
        "number_of_pages",
        "publication_date",
        # "authors",
        # "translators",
        # "category",
        "publisher",
        "language",
        "inventory",
        "is_active",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "modified_at",
    )

    list_per_page = 10
    search_fields = ("name",)
    ordering = ("-created_at",)
