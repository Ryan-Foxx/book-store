import datetime
from unittest.mock import patch

import pytest
from apps.books.models import Book
from apps.books.utils.paths import book_avatar_upload_path
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError


@pytest.mark.django_db
class TestBookModel:

    def test_create_book_successful(self, book_factory, language_factory, publisher_factory):
        language = language_factory(name="Persian")
        publisher = publisher_factory(name="Cheshmeh")

        book = book_factory(
            name="The Metamorphosis",
            price=120000,
            number_of_pages=150,
            publication_date=datetime.date(2024, 5, 20),
            language=language,
            publisher=publisher,
            inventory=25,
            is_active=True,
        )

        assert book.id is not None
        assert book.name == "The Metamorphosis"
        assert book.price == 120000
        assert book.number_of_pages == 150
        assert book.publication_date == datetime.date(2024, 5, 20)
        assert book.language == language
        assert book.publisher == publisher
        assert book.inventory == 25
        assert book.is_active is True
        assert bool(book.avatar) is False
        assert book.created_at is not None
        assert book.modified_at is not None

    def test_book_name_must_be_unique(self, book_factory):
        book_factory(name="Clean Code")

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                book_factory(name="Clean Code")

    def test_book_str_returns_name(self, book_factory):
        book = book_factory(name="Refactoring")

        assert str(book) == "Refactoring"

    def test_book_default_values(self, language_factory):
        book = Book.objects.create(
            name="Default Values Book", publication_date=datetime.date(2025, 1, 1), language=language_factory()
        )

        assert book.price == 0
        assert book.inventory == 0
        assert book.is_active is False
        assert book.publisher is None
        assert book.number_of_pages is None
        assert bool(book.avatar) is False

    def test_book_many_to_many_relationships(self, book_factory, author_factory, translator_factory, category_factory):
        author_1 = author_factory()
        author_2 = author_factory()
        translator = translator_factory()
        category_1 = category_factory()
        category_2 = category_factory()

        book = book_factory(authors=[author_1, author_2], translators=[translator], category=[category_1, category_2])

        assert set(book.authors.all()) == {author_1, author_2}
        assert set(book.translators.all()) == {translator}
        assert set(book.category.all()) == {category_1, category_2}

    def test_book_protected_deletion_on_language(self, book_factory, language_factory):
        language = language_factory()
        book_factory(language=language)

        with pytest.raises(ProtectedError):
            language.delete()

    def test_book_protected_deletion_on_publisher(self, book_factory, publisher_factory):
        publisher = publisher_factory()
        book_factory(publisher=publisher)

        with pytest.raises(ProtectedError):
            publisher.delete()

    def test_book_avatar_upload_path_returns_expected_path(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = book_avatar_upload_path(instance=None, filename="cover.jpg")

        assert path == "books/books/avatars/fixeduuidhex.jpg"

    def test_book_avatar_upload_path_preserves_file_extension(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = book_avatar_upload_path(instance=None, filename="cover.webp")

        assert path == "books/books/avatars/fixeduuidhex.webp"
