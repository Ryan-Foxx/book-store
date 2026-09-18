from apps.books.models import Publisher


def get_public_publisher_list_queryset():
    return Publisher.objects.only("id", "name", "avatar").order_by("-created_at")


def get_public_publisher_detail_queryset():
    return Publisher.objects.only("id", "name", "avatar", "about")


def get_admin_publisher_queryset():
    return Publisher.objects.all().order_by("-modified_at")
