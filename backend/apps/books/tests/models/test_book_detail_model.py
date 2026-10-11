from unittest.mock import patch

import pytest
from apps.books.models import BookDetail
from apps.books.utils.paths import book_detail_image_upload_path
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestBookDetailModel:

    def test_create_text_section_book_detail_successful(self, book_detail_factory, book_factory):
        book = book_factory(name="Clean Architecture")
        detail = book_detail_factory(
            book=book,
            order=1,
            section_type=BookDetail.SECTION_TYPE_TEXT,
            text="Detailed overview of clean architecture principles.",
            image=None,
        )

        assert detail.id is not None
        assert detail.book == book
        assert detail.order == 1
        assert detail.section_type == BookDetail.SECTION_TYPE_TEXT
        assert detail.text == "Detailed overview of clean architecture principles."
        assert bool(detail.image) is False
        assert detail.created_at is not None
        assert detail.modified_at is not None

    def test_create_image_section_book_detail_successful(self, book_detail_factory, book_factory):
        book = book_factory(name="Design Patterns")
        image = SimpleUploadedFile("diagram.png", b"dummy_data", content_type="image/png")

        detail = book_detail_factory(
            book=book,
            order=2,
            section_type=BookDetail.SECTION_TYPE_IMAGE,
            text="",
            image=image,
        )

        assert detail.id is not None
        assert detail.book == book
        assert detail.order == 2
        assert detail.section_type == BookDetail.SECTION_TYPE_IMAGE
        assert detail.text == ""
        assert bool(detail.image) is True

        detail.image.storage.delete(detail.image.name)

    def test_book_detail_str_returns_expected_format(self, book_detail_factory, book_factory):
        book = book_factory(name="Domain-Driven Design")
        detail = book_detail_factory(
            book=book,
            order=3,
            section_type=BookDetail.SECTION_TYPE_TEXT,
        )

        assert str(detail) == "Domain-Driven Design - text #3"

    def test_book_detail_default_values(self, book_factory):
        book = book_factory()
        detail = BookDetail.objects.create(
            book=book,
            section_type=BookDetail.SECTION_TYPE_TEXT,
        )

        assert detail.order == 0
        assert detail.text == ""
        assert bool(detail.image) is False

    def test_book_cascade_deletion_deletes_related_details(self, book_factory, book_detail_factory):
        book = book_factory()
        detail_1 = book_detail_factory(book=book, order=1)
        detail_2 = book_detail_factory(book=book, order=2)

        assert BookDetail.objects.filter(book=book).count() == 2

        book.delete()

        assert BookDetail.objects.filter(id__in=[detail_1.id, detail_2.id]).count() == 0

    def test_book_detail_image_upload_path_returns_expected_path(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = book_detail_image_upload_path(instance=None, filename="infographic.jpg")

        assert path == "books/book-details/images/fixeduuidhex.jpg"

    def test_book_detail_image_upload_path_preserves_file_extension(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = book_detail_image_upload_path(instance=None, filename="diagram.webp")

        assert path == "books/book-details/images/fixeduuidhex.webp"
