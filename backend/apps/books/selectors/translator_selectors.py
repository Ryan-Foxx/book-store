from apps.books.models import Translator


def get_admin_translator_queryset():
    return Translator.objects.all().order_by("-modified_at")
