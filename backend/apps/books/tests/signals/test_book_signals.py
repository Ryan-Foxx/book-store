import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestBookSignals:

    def test_avatar_deleted_from_storage_when_book_deleted(self, book_factory):
        avatar = SimpleUploadedFile("book_cover.png", b"dummy_content", content_type="image/png")
        book = book_factory(avatar=avatar)

        storage = book.avatar.storage
        avatar_name = book.avatar.name

        assert storage.exists(avatar_name) is True

        book.delete()

        assert storage.exists(avatar_name) is False

    def test_old_avatar_deleted_when_new_avatar_uploaded(self, book_factory):
        old_avatar = SimpleUploadedFile("old_cover.png", b"old_content", content_type="image/png")
        book = book_factory(avatar=old_avatar)

        storage = book.avatar.storage
        old_avatar_name = book.avatar.name

        assert storage.exists(old_avatar_name) is True

        new_avatar = SimpleUploadedFile("new_cover.png", b"new_content", content_type="image/png")
        book.avatar = new_avatar
        book.save()

        assert storage.exists(old_avatar_name) is False
        assert storage.exists(book.avatar.name) is True

        storage.delete(book.avatar.name)

    def test_avatar_not_deleted_when_other_fields_updated(self, book_factory):
        avatar = SimpleUploadedFile("book_cover.png", b"dummy_content", content_type="image/png")
        book = book_factory(avatar=avatar)

        storage = book.avatar.storage
        avatar_name = book.avatar.name

        book.price = 99000
        book.save()

        assert storage.exists(avatar_name) is True

        storage.delete(avatar_name)
