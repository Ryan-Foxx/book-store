import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestPublisherSignals:

    def test_avatar_deleted_from_storage_when_publisher_deleted(self, publisher_factory):
        avatar = SimpleUploadedFile("publisher_logo.png", b"dummy_content", content_type="image/png")
        publisher = publisher_factory(avatar=avatar)

        storage = publisher.avatar.storage
        avatar_name = publisher.avatar.name

        assert storage.exists(avatar_name) is True

        publisher.delete()

        assert storage.exists(avatar_name) is False

    def test_old_avatar_deleted_when_new_avatar_uploaded(self, publisher_factory):
        old_avatar = SimpleUploadedFile("old_logo.png", b"old_content", content_type="image/png")
        publisher = publisher_factory(avatar=old_avatar)

        storage = publisher.avatar.storage
        old_avatar_name = publisher.avatar.name

        assert storage.exists(old_avatar_name) is True

        new_avatar = SimpleUploadedFile("new_logo.png", b"new_content", content_type="image/png")
        publisher.avatar = new_avatar
        publisher.save()

        assert storage.exists(old_avatar_name) is False
        assert storage.exists(publisher.avatar.name) is True

        storage.delete(publisher.avatar.name)

    def test_avatar_not_deleted_when_other_fields_updated(self, publisher_factory):
        avatar = SimpleUploadedFile("publisher_logo.png", b"dummy_content", content_type="image/png")
        publisher = publisher_factory(avatar=avatar)

        storage = publisher.avatar.storage
        avatar_name = publisher.avatar.name

        publisher.about = "Updated about section"
        publisher.save()

        assert storage.exists(avatar_name) is True

        storage.delete(avatar_name)
