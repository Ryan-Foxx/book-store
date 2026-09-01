from unittest.mock import patch

import pytest
from apps.books.models import Publisher
from apps.books.utils.paths import publisher_avatar_upload_path
from django.db import IntegrityError, transaction


@pytest.mark.django_db
class TestPublisherModel:

    def test_create_publisher_successful(self, publisher_factory):
        publisher = publisher_factory(name="Penguin Books", about="Major international publisher")

        assert publisher.id is not None
        assert publisher.name == "Penguin Books"
        assert publisher.about == "Major international publisher"
        assert bool(publisher.avatar) is False
        assert publisher.created_at is not None
        assert publisher.modified_at is not None

    def test_publisher_name_must_be_unique(self, publisher_factory):
        publisher_factory(name="Penguin Books")

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                publisher_factory(name="Penguin Books")

    def test_publisher_str_returns_name(self, publisher_factory):
        publisher = publisher_factory(name="Bloomsbury")

        assert str(publisher) == "Bloomsbury"

    def test_publisher_about_defaults_to_empty_string(self):
        publisher = Publisher.objects.create(name="Publisher Without About")
        assert publisher.about == ""

    def test_publisher_avatar_upload_path_returns_expected_path(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = publisher_avatar_upload_path(instance=None, filename="logo.jpg")

        assert path == "books/publishers/avatars/fixeduuidhex.jpg"

    def test_publisher_avatar_upload_path_preserves_file_extension(self):
        with patch("apps.books.utils.paths.uuid.uuid4") as mock_uuid4:
            mock_uuid4.return_value.hex = "fixeduuidhex"

            path = publisher_avatar_upload_path(instance=None, filename="logo.webp")

        assert path == "books/publishers/avatars/fixeduuidhex.webp"
