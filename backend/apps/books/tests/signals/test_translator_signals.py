import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestTranslatorSignals:

    def test_avatar_deleted_from_storage_when_translator_deleted(self, translator_factory):
        avatar = SimpleUploadedFile("avatar.jpg", b"dummy_content", content_type="image/jpeg")
        translator = translator_factory(avatar=avatar)

        storage = translator.avatar.storage
        avatar_name = translator.avatar.name

        assert storage.exists(avatar_name) is True

        translator.delete()

        assert storage.exists(avatar_name) is False

    def test_old_avatar_deleted_when_new_avatar_uploaded(self, translator_factory):
        old_avatar = SimpleUploadedFile("old.jpg", b"old_content", content_type="image/jpeg")
        translator = translator_factory(avatar=old_avatar)

        storage = translator.avatar.storage
        old_avatar_name = translator.avatar.name

        assert storage.exists(old_avatar_name) is True

        new_avatar = SimpleUploadedFile("new.jpg", b"new_content", content_type="image/jpeg")
        translator.avatar = new_avatar
        translator.save()

        assert storage.exists(old_avatar_name) is False
        assert storage.exists(translator.avatar.name) is True

        storage.delete(translator.avatar.name)

    def test_avatar_not_deleted_when_other_fields_updated(self, translator_factory):
        avatar = SimpleUploadedFile("avatar.jpg", b"dummy_content", content_type="image/jpeg")
        translator = translator_factory(avatar=avatar)

        storage = translator.avatar.storage
        avatar_name = translator.avatar.name

        translator.about = "Updated about"
        translator.save()

        assert storage.exists(avatar_name) is True

        storage.delete(avatar_name)
