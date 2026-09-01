from apps.books.utils.paths import (
    author_avatar_upload_path,
    book_avatar_upload_path,
    publisher_avatar_upload_path,
    translator_avatar_upload_path,
)
from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=author_avatar_upload_path, null=True, blank=True)
    about = models.TextField(blank=True)
    biography = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Award(models.Model):
    authors = models.ManyToManyField(Author, blank=True, related_name="awards")
    title = models.CharField(max_length=255, unique=True)
    year_received = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Translator(models.Model):
    name = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=translator_avatar_upload_path, null=True, blank=True)
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=publisher_avatar_upload_path, null=True, blank=True)
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=500, unique=True)
    avatar = models.ImageField(upload_to=book_avatar_upload_path, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=0, default=0)
    number_of_pages = models.PositiveSmallIntegerField(null=True, blank=True)
    publication_date = models.DateField()
    authors = models.ManyToManyField(Author, blank=True, related_name="books")
    translators = models.ManyToManyField(Translator, blank=True, related_name="books")
    category = models.ManyToManyField(Category, related_name="books")
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, null=True, blank=True, related_name="books")
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="books")
    inventory = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
