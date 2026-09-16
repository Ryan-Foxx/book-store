from apps.books.models import Publisher


def get_admin_publisher_queryset():
    return Publisher.objects.all().order_by("-modified_at")
