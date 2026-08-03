from apps.books.models import Author
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
