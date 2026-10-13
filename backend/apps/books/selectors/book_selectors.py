from apps.books.models import Book, BookDetail, Favorite
from django.db.models import Avg, Count, DecimalField, Exists, OuterRef, Prefetch, Value
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
        .select_related("language")
        .only(
            "id",
            "name",
            "avatar",
            "price",
            "language",
        )
        .order_by("-created_at")
    )


def get_public_book_detail_queryset(user=None):
    queryset = Book.objects.annotate(
        rating_average=Coalesce(
            Round(Avg("ratings__score"), 1),
            Value(0.0),
            output_field=DecimalField(max_digits=3, decimal_places=1),
        ),
        ratings_count=Count("ratings"),
    )

    if user and user.is_authenticated:
        favorite_subquery = Favorite.objects.filter(
            user=user,
            book=OuterRef("pk"),
        )
        queryset = queryset.annotate(is_favorited=Exists(favorite_subquery))
    else:
        queryset = queryset.annotate(is_favorited=Value(False))

    return (
        queryset.select_related("publisher", "language")
        .prefetch_related(
            "authors",
            "translators",
            "category",
            Prefetch("details", queryset=BookDetail.objects.order_by("order")),
        )
        .only(
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
    )
