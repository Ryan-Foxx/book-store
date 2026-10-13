from apps.books.models import Book
from django.db.models import Avg, Count, DecimalField, Value
from django.db.models.functions import Coalesce, Round


def get_public_book_list_queryset():
    return (
        Book.objects.annotate(
            rating_average=Coalesce(
                Round(Avg("ratings__score"), 1),
                Value(0.0),
                output_field=DecimalField(max_digits=3, decimal_places=1),
            )
        )
        .only(
            "id",
            "name",
            "avatar",
            "price",
            "language",
        )
        .order_by("-created_at")
    )


def get_public_book_detail_queryset():
    return Book.objects.annotate(
        rating_average=Coalesce(
            Round(Avg("ratings__score"), 1),
            Value(0.0),
            output_field=DecimalField(max_digits=3, decimal_places=1),
        ),
        ratings_count=Count("ratings"),
    ).only(
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
