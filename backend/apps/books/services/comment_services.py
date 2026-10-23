from apps.books.models import Book, Comment
from apps.users.models import User


def create_comment(*, user: User, book: Book, body: str) -> Comment:

    comment = Comment.objects.create(
        user=user,
        book=book,
        body=body,
    )
    return comment
