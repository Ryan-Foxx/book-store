from django.contrib import admin

from .models import Author, Book, Category, ContentFormat, Language, Publisher, Translator


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    pass


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(ContentFormat)
class ContentFormatAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass
