import pytest
from apps.books.models import BookDetail
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestBookDetailSignals:

    def test_image_deleted_from_storage_when_book_detail_deleted(self, book_detail_factory):
        image_file = SimpleUploadedFile("detail_image.png", b"dummy_content", content_type="image/png")
        detail = book_detail_factory(
            section_type=BookDetail.SECTION_TYPE_IMAGE,
            image=image_file,
        )

        storage = detail.image.storage
        image_name = detail.image.name

        assert storage.exists(image_name) is True

        detail.delete()

        assert storage.exists(image_name) is False

    def test_old_image_deleted_when_new_image_uploaded(self, book_detail_factory):
        old_image = SimpleUploadedFile("old_detail.png", b"old_content", content_type="image/png")
        detail = book_detail_factory(
            section_type=BookDetail.SECTION_TYPE_IMAGE,
            image=old_image,
        )

        storage = detail.image.storage
        old_image_name = detail.image.name

        assert storage.exists(old_image_name) is True

        new_image = SimpleUploadedFile("new_detail.png", b"new_content", content_type="image/png")
        detail.image = new_image
        detail.save()

        assert storage.exists(old_image_name) is False
        assert storage.exists(detail.image.name) is True

        storage.delete(detail.image.name)

    def test_image_not_deleted_when_other_fields_updated(self, book_detail_factory):
        image_file = SimpleUploadedFile("keep_detail.png", b"keep_content", content_type="image/png")
        detail = book_detail_factory(
            section_type=BookDetail.SECTION_TYPE_IMAGE,
            image=image_file,
        )

        storage = detail.image.storage
        image_name = detail.image.name

        detail.order = 99
        detail.save()

        assert storage.exists(image_name) is True

        # پاک‌سازی
        storage.delete(image_name)
