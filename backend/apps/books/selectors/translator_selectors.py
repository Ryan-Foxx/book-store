from apps.books.models import Translator


def get_public_translator_list_queryset():
    return Translator.objects.only("id", "name", "avatar").order_by("-created_at")


def get_public_translator_detail_queryset():
    return Translator.objects.only("id", "name", "avatar", "about")


def get_admin_translator_queryset():
    return Translator.objects.all().order_by("-modified_at")
