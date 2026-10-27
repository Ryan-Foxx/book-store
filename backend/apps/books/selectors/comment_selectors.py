from apps.books.models import Comment


def get_public_comment_list_queryset(*, book_id: int):
    return (
        Comment.objects.filter(
            book_id=book_id,
            book__is_active=True,
            status=Comment.COMMENT_STATUS_APPROVED,
        )
        .select_related("user", "user__profile")
        .only("id", "body", "created_at", "user__username", "user__profile__avatar")
        .order_by("-created_at")
    )


def get_public_comment_queryset():
    return Comment.objects.all()


def get_admin_comment_list_queryset():
    return Comment.objects.all().order_by("-modified_at")


def get_admin_comment_queryset():
    return Comment.objects.all()
