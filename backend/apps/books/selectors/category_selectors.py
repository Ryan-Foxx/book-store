from apps.books.models import Category


def get_admin_category_queryset():
    return Category.objects.all().order_by("-modified_at")
