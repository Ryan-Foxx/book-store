import pytest
from apps.books.models import Category
from django.db import IntegrityError, transaction


@pytest.mark.django_db
class TestCategoryModel:

    def test_create_category_successful(self, category_factory):
        category = category_factory(
            title="Science Fiction", description="Books about futuristic science and technology"
        )

        assert category.id is not None
        assert category.title == "Science Fiction"
        assert category.description == "Books about futuristic science and technology"
        assert category.created_at is not None
        assert category.modified_at is not None

    def test_category_title_must_be_unique(self, category_factory):
        category_factory(title="Fantasy")

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                category_factory(title="Fantasy")

    def test_category_str_returns_title(self, category_factory):
        category = category_factory(title="History")

        assert str(category) == "History"

    def test_category_description_defaults_to_empty_string(self):
        category = Category.objects.create(title="Novel")

        assert category.description == ""
