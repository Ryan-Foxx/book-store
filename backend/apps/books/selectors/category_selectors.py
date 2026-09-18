from apps.books.models import Category


def get_public_category_list_queryset():
    return Category.objects.only("id", "title").order_by("-created_at")


def get_public_category_detail_queryset():
    return Category.objects.only("id", "title", "description")


def get_admin_category_queryset():
    return Category.objects.all().order_by("-modified_at")
