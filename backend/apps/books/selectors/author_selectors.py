from apps.books.models import Author, Award
from django.db.models import Prefetch

def get_public_author_list_queryset():
    return Author.objects.only("id", "name", "avatar").order_by("-created_at")


def get_public_author_detail_queryset():
    return Author.objects.only("id", "name", "avatar", "about", "biography").prefetch_related(
        Prefetch("awards", queryset=Award.objects.only("id", "title", "year_received"))
    )


def get_admin_author_queryset():
    return Author.objects.all().order_by("-modified_at")
