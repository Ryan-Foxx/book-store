from apps.books.models import Award


def get_admin_award_queryset():
    return Award.objects.all().order_by("-modified_at").prefetch_related("authors")
