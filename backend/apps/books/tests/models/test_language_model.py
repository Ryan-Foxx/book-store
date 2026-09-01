import pytest
from apps.books.models import Language
from django.db import IntegrityError, transaction


@pytest.mark.django_db
class TestLanguageModel:

    def test_create_language_successful(self, language_factory):
        language = language_factory(name="Persian")

        assert language.id is not None
        assert language.name == "Persian"
        assert language.created_at is not None
        assert language.modified_at is not None

    def test_language_name_must_be_unique(self, language_factory):
        language_factory(name="English")

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                language_factory(name="English")

    def test_language_str_returns_name(self, language_factory):
        language = language_factory(name="French")

        assert str(language) == "French"
