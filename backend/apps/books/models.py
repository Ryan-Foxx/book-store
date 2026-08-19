from apps.books.utils.paths import author_avatar_upload_path
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
