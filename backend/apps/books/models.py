from apps.books.utils.paths import (
    author_avatar_upload_path,
    book_avatar_upload_path,
    book_detail_image_upload_path,
    publisher_avatar_upload_path,
    translator_avatar_upload_path,
)
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

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


class BookDetail(models.Model):
    SECTION_TYPE_TEXT = "text"
    SECTION_TYPE_IMAGE = "image"

    SECTION_TYPES = [
        (SECTION_TYPE_TEXT, "Text"),
        (SECTION_TYPE_IMAGE, "Image"),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="details")
    order = models.PositiveSmallIntegerField(default=0)
    section_type = models.CharField(max_length=5, choices=SECTION_TYPES)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to=book_detail_image_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.name} - {self.section_type} #{self.order}"


class Comment(models.Model):
    COMMENT_STATUS_WAITING = "w"
    COMMENT_STATUS_APPROVED = "a"
    COMMENT_STATUS_NOT_APPROVED = "na"
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, "Waiting"),
        (COMMENT_STATUS_APPROVED, "Approved"),
        (COMMENT_STATUS_NOT_APPROVED, "Not Approved"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "book"], name="unique_books_favorite_user_book")]

    def __str__(self):
        return f"{self.user} - {self.book}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "book"], name="unique_books_rating_user_book")]

    def __str__(self):
        return f"{self.user} rated {self.book} -> {self.score}"
