import pytest
from apps.books.models import Favorite
from django.db import IntegrityError, transaction


@pytest.mark.django_db
class TestFavoriteModel:

    def test_create_favorite_successful(self, favorite_factory, user_factory, book_factory):
        user = user_factory(username="favorite_user")
        book = book_factory(name="Clean Code")

        favorite = favorite_factory(
            user=user,
            book=book,
        )

        assert favorite.id is not None
        assert favorite.user == user
        assert favorite.book == book
        assert favorite.created_at is not None
        assert favorite.modified_at is not None

    def test_favorite_str_returns_expected_value(self, favorite_factory, user_factory, book_factory):
        user = user_factory(username="john")
        book = book_factory(name="Refactoring")

        favorite = favorite_factory(
            user=user,
            book=book,
        )

        assert str(favorite) == f"{user} - {book}"

    def test_favorite_user_and_book_combination_must_be_unique(
        self,
        favorite_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book = book_factory()

        favorite_factory(user=user, book=book)

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                favorite_factory(user=user, book=book)

    def test_same_user_can_favorite_different_books(
        self,
        favorite_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book_1 = book_factory(name="Book One")
        book_2 = book_factory(name="Book Two")

        favorite_1 = favorite_factory(user=user, book=book_1)
        favorite_2 = favorite_factory(user=user, book=book_2)

        assert favorite_1.id != favorite_2.id
        assert Favorite.objects.filter(user=user).count() == 2
        assert set(Favorite.objects.filter(user=user).values_list("book_id", flat=True)) == {
            book_1.id,
            book_2.id,
        }

    def test_different_users_can_favorite_same_book(
        self,
        favorite_factory,
        user_factory,
        book_factory,
    ):
        user_1 = user_factory(username="user_one")
        user_2 = user_factory(username="user_two")
        book = book_factory(name="Shared Favorite Book")

        favorite_1 = favorite_factory(user=user_1, book=book)
        favorite_2 = favorite_factory(user=user_2, book=book)

        assert favorite_1.id != favorite_2.id
        assert Favorite.objects.filter(book=book).count() == 2
        assert set(Favorite.objects.filter(book=book).values_list("user_id", flat=True)) == {
            user_1.id,
            user_2.id,
        }

    def test_deleting_user_deletes_related_favorites(
        self,
        favorite_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book = book_factory()

        favorite = favorite_factory(user=user, book=book)

        assert Favorite.objects.filter(id=favorite.id).exists() is True

        user.delete()

        assert Favorite.objects.filter(id=favorite.id).exists() is False

    def test_deleting_book_deletes_related_favorites(
        self,
        favorite_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book = book_factory()

        favorite = favorite_factory(user=user, book=book)

        assert Favorite.objects.filter(id=favorite.id).exists() is True

        book.delete()

        assert Favorite.objects.filter(id=favorite.id).exists() is False

    def test_user_favorites_reverse_relationship(
        self,
        favorite_factory,
        user_factory,
        book_factory,
    ):
        user = user_factory()
        book_1 = book_factory(name="First Book")
        book_2 = book_factory(name="Second Book")

        favorite_factory(user=user, book=book_1)
        favorite_factory(user=user, book=book_2)

        assert user.favorites.count() == 2
        assert set(user.favorites.values_list("book_id", flat=True)) == {
            book_1.id,
            book_2.id,
        }

    def test_book_favorites_reverse_relationship(
        self,
        favorite_factory,
        user_factory,
        book_factory,
    ):
        user_1 = user_factory(username="first_user")
        user_2 = user_factory(username="second_user")
        book = book_factory()

        favorite_factory(user=user_1, book=book)
        favorite_factory(user=user_2, book=book)

        assert book.favorites.count() == 2
        assert set(book.favorites.values_list("user_id", flat=True)) == {
            user_1.id,
            user_2.id,
        }
