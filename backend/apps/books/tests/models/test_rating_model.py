import pytest
from apps.books.models import Rating
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction


@pytest.mark.django_db
class TestRatingModel:

    def test_create_rating_successful(self, rating_factory, user_factory, book_factory):
        user = user_factory(username="rating_user")
        book = book_factory(name="Clean Code")

        rating = rating_factory(
            user=user,
            book=book,
            score=4,
        )

        assert rating.id is not None
        assert rating.user == user
        assert rating.book == book
        assert rating.score == 4
        assert rating.created_at is not None
        assert rating.modified_at is not None

    def test_rating_str_returns_expected_value(
        self,
        rating_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory(username="john")
        book = book_factory(name="Refactoring")

        rating = rating_factory(
            user=user,
            book=book,
            score=5,
        )

        assert str(rating) == f"{user} rated {book} -> 5"

    @pytest.mark.parametrize("score", [1, 2, 3, 4, 5])
    def test_rating_accepts_valid_scores(
        self,
        rating_factory,
        score,
    ):
        rating = rating_factory(score=score)

        assert rating.score == score

    @pytest.mark.parametrize("score", [0, 6, 10, -1])
    def test_rating_rejects_invalid_scores(
        self,
        user_factory,
        book_factory,
        score,
    ):
        user = user_factory()
        book = book_factory()

        rating = Rating(
            user=user,
            book=book,
            score=score,
        )

        with pytest.raises(ValidationError):
            rating.full_clean()

    def test_rating_user_and_book_combination_must_be_unique(
        self,
        rating_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book = book_factory()

        rating_factory(
            user=user,
            book=book,
            score=4,
        )

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                rating_factory(
                    user=user,
                    book=book,
                    score=5,
                )

    def test_same_user_can_rate_different_books(
        self,
        rating_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book_1 = book_factory(name="Book One")
        book_2 = book_factory(name="Book Two")

        rating_1 = rating_factory(
            user=user,
            book=book_1,
            score=4,
        )
        rating_2 = rating_factory(
            user=user,
            book=book_2,
            score=5,
        )

        assert rating_1.id != rating_2.id
        assert Rating.objects.filter(user=user).count() == 2
        assert set(Rating.objects.filter(user=user).values_list("book_id", flat=True)) == {
            book_1.id,
            book_2.id,
        }

    def test_different_users_can_rate_same_book(
        self,
        rating_factory,
        user_factory,
        book_factory,
    ):
        user_1 = user_factory(username="first_user")
        user_2 = user_factory(username="second_user")
        book = book_factory(name="Shared Rating Book")

        rating_1 = rating_factory(
            user=user_1,
            book=book,
            score=3,
        )
        rating_2 = rating_factory(
            user=user_2,
            book=book,
            score=5,
        )

        assert rating_1.id != rating_2.id
        assert Rating.objects.filter(book=book).count() == 2
        assert set(Rating.objects.filter(book=book).values_list("user_id", flat=True)) == {
            user_1.id,
            user_2.id,
        }

    def test_deleting_user_deletes_related_ratings(
        self,
        rating_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book = book_factory()

        rating = rating_factory(
            user=user,
            book=book,
            score=4,
        )

        assert Rating.objects.filter(id=rating.id).exists() is True

        user.delete()

        assert Rating.objects.filter(id=rating.id).exists() is False

    def test_deleting_book_deletes_related_ratings(
        self,
        rating_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book = book_factory()

        rating = rating_factory(
            user=user,
            book=book,
            score=4,
        )

        assert Rating.objects.filter(id=rating.id).exists() is True

        book.delete()

        assert Rating.objects.filter(id=rating.id).exists() is False

    def test_user_ratings_reverse_relationship(
        self,
        rating_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book_1 = book_factory(name="First Book")
        book_2 = book_factory(name="Second Book")

        rating_factory(user=user, book=book_1, score=3)
        rating_factory(user=user, book=book_2, score=5)

        assert user.ratings.count() == 2
        assert set(user.ratings.values_list("book_id", flat=True)) == {
            book_1.id,
            book_2.id,
        }

    def test_book_ratings_reverse_relationship(
        self,
        rating_factory,
        user_factory,
        book_factory,
    ):
        user_1 = user_factory(username="first_user")
        user_2 = user_factory(username="second_user")
        book = book_factory()

        rating_factory(user=user_1, book=book, score=3)
        rating_factory(user=user_2, book=book, score=5)

        assert book.ratings.count() == 2
        assert set(book.ratings.values_list("user_id", flat=True)) == {
            user_1.id,
            user_2.id,
        }
