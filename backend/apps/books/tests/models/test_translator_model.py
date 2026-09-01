from unittest.mock import patch

import pytest
from apps.books.models import Translator
from apps.books.utils.paths import translator_avatar_upload_path
from django.db import IntegrityError, transaction


@pytest.mark.django_db
class TestTranslatorModel:

    def test_create_translator_successful(self, translator_factory):
        translator = translator_factory(name="J. K. Rowling", about="Experienced translator")

        assert translator.id is not None
        assert translator.name == "J. K. Rowling"
        assert translator.about == "Experienced translator"
        assert bool(translator.avatar) is False
        assert translator.created_at is not None
        assert translator.modified_at is not None

    def test_translator_about_defaults_to_empty_string(self):
        translator = Translator.objects.create(name="Translator Without About")
        assert translator.about == ""

    def test_translator_name_must_be_unique(self, translator_factory):
        translator_factory(name="J. K. Rowling")

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                translator_factory(name="J. K. Rowling")

    def test_translator_str_returns_name(self, translator_factory):
        translator = translator_factory(name="J. K. Rowling")

        assert str(translator) == "J. K. Rowling"

    def test_translator_avatar_upload_path_returns_expected_path(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = translator_avatar_upload_path(instance=None, filename="avatar.jpg")

        assert path == "books/translators/avatars/fixeduuidhex.jpg"

    def test_translator_avatar_upload_path_preserves_file_extension(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = translator_avatar_upload_path(instance=None, filename="profile.png")

        assert path == "books/translators/avatars/fixeduuidhex.png"
