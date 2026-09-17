from apps.books.models import Language


def get_admin_language_queryset():
    return Language.objects.all().order_by("-modified_at")
