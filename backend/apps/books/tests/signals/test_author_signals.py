import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestAuthorSignals:

    def test_delete_old_avatar_on_change_deletes_previous_file(self, tmp_path, settings, author_factory):
        settings.MEDIA_ROOT = tmp_path

        old_avatar = SimpleUploadedFile("old.jpg", b"old-file", content_type="image/jpeg")
        author = author_factory(name="Author 1", avatar=old_avatar)

        old_avatar_path = author.avatar.path

        assert os.path.exists(old_avatar_path)

        new_avatar = SimpleUploadedFile("new.jpg", b"new-file", content_type="image/jpeg")
        author.avatar = new_avatar
        author.save()

        assert not os.path.exists(old_avatar_path)

    def test_delete_old_avatar_on_change_does_not_delete_when_avatar_is_unchanged(
        self, tmp_path, settings, author_factory
    ):
        settings.MEDIA_ROOT = tmp_path

        avatar = SimpleUploadedFile("same.jpg", b"file-data", content_type="image/jpeg")
        author = author_factory(name="Author 1", avatar=avatar)

        avatar_path = author.avatar.path

        author.name = "Updated Name"
        author.save()

        assert os.path.exists(avatar_path)

    def test_delete_avatar_on_author_delete_removes_file(self, tmp_path, settings, author_factory):
        settings.MEDIA_ROOT = tmp_path

        avatar = SimpleUploadedFile("delete.jpg", b"file-data", content_type="image/jpeg")
        author = author_factory(name="Author 1", avatar=avatar)

        avatar_path = author.avatar.path

        assert os.path.exists(avatar_path)

        author.delete()

        assert not os.path.exists(avatar_path)

    def test_delete_avatar_on_author_delete_without_avatar_does_nothing(self, author_factory):
        author = author_factory(name="Author Without Avatar")

        author.delete()
