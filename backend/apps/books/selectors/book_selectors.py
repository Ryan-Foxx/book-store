from apps.books.models import Book


def get_public_book_list_queryset():
    return Book.objects.only(
        "id",
        "name",
        "avatar",
        "price",
    ).order_by("-created_at")


def get_public_book_detail_queryset():
    return Book.objects.only(
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
    )
