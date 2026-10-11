import pytest
from apps.books.models import Comment


@pytest.mark.django_db
class TestCommentModel:

    def test_create_comment_successful(self, comment_factory, user_factory, book_factory):
        user = user_factory(username="johndoe")
        book = book_factory(name="Design Patterns")

        comment = comment_factory(
            user=user,
            book=book,
            body="An absolute masterpiece on software engineering!",
            status=Comment.COMMENT_STATUS_APPROVED,
        )

        assert comment.id is not None
        assert comment.user == user
        assert comment.book == book
        assert comment.body == "An absolute masterpiece on software engineering!"
        assert comment.status == Comment.COMMENT_STATUS_APPROVED
        assert comment.created_at is not None
        assert comment.modified_at is not None

    def test_comment_default_values(self, user_factory, book_factory):
        user = user_factory()
        book = book_factory()

        comment = Comment.objects.create(
            user=user,
            book=book,
            body="Just a basic pending review.",
        )

        assert comment.status == Comment.COMMENT_STATUS_WAITING
        assert comment.status == "w"

    @pytest.mark.parametrize(
        "status_code",
        [
            Comment.COMMENT_STATUS_WAITING,
            Comment.COMMENT_STATUS_APPROVED,
            Comment.COMMENT_STATUS_NOT_APPROVED,
        ],
    )
    def test_comment_choices(self, comment_factory, status_code):
        comment = comment_factory(status=status_code)

        assert comment.status == status_code

    def test_comment_cascade_deletion_on_user_delete(self, comment_factory, user_factory):
        user = user_factory()
        comment = comment_factory(user=user)

        assert Comment.objects.filter(id=comment.id).exists() is True

        user.delete()

        assert Comment.objects.filter(id=comment.id).exists() is False

    def test_comment_cascade_deletion_on_book_delete(self, comment_factory, book_factory):
        book = book_factory()
        comment = comment_factory(book=book)

        assert Comment.objects.filter(id=comment.id).exists() is True

        book.delete()

        assert Comment.objects.filter(id=comment.id).exists() is False

    def test_user_can_have_multiple_comments_on_same_book(self, comment_factory, user_factory, book_factory):
        user = user_factory()
        book = book_factory()

        comment_1 = comment_factory(user=user, book=book, body="First comment")
        comment_2 = comment_factory(user=user, book=book, body="Second follow-up comment")

        assert comment_1.id != comment_2.id
        assert Comment.objects.filter(user=user, book=book).count() == 2
