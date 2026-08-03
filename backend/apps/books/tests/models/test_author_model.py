from unittest.mock import patch

import pytest
from apps.books.utils.paths import author_avatar_upload_path
from django.db import IntegrityError


@pytest.mark.django_db
class TestAuthorModel:

    def test_author_name_must_be_unique(self, author_factory):
        author_factory(name="J. K. Rowling")

        with pytest.raises(IntegrityError):
            author_factory(name="J. K. Rowling")

    def test_author_str_returns_name(self, author_factory):
        author = author_factory(name="J. K. Rowling")

        assert str(author) == "J. K. Rowling"

    def test_author_avatar_upload_path_returns_expected_path(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = author_avatar_upload_path(instance=None, filename="avatar.jpg")

        assert path == "authors/avatars/fixeduuidhex.jpg"

    def test_author_avatar_upload_path_preserves_file_extension(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = author_avatar_upload_path(instance=None, filename="profile.png")

        assert path == "authors/avatars/fixeduuidhex.png"
