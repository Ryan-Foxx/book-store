from apps.books.models import Author


def get_public_author_list_queryset():
    return Author.objects.only("id", "name", "avatar").order_by("-created_at")


def get_public_author_detail_queryset():
    return Author.objects.only("id", "name", "avatar", "about", "biography")
