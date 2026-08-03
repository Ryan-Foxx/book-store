from datetime import timedelta

import pytest
from apps.books.models import Author
from apps.books.selectors.author_selectors import (
    get_public_author_detail_queryset,
    get_public_author_list_queryset,
)
from django.utils import timezone


@pytest.fixture
def list_deferred_fields():
    def get(author_id):
        author_from_db = get_public_author_list_queryset().get(id=author_id)
        return author_from_db.get_deferred_fields()

    return get


@pytest.fixture
def detail_deferred_fields():
    def get(author_id):
        author_from_db = get_public_author_detail_queryset().get(id=author_id)
        return author_from_db.get_deferred_fields()

    return get


@pytest.mark.django_db
class TestGetAuthorListQueryset:

    def test_get_author_list_queryset_returns_authors_ordered_by_created_at_desc(self, author_factory):
        now = timezone.now()

        old = author_factory(name="Old Author")
        Author.objects.filter(id=old.id).update(created_at=now - timedelta(days=2))

        new = author_factory(name="New Author")
        Author.objects.filter(id=new.id).update(created_at=now)

        queryset = get_public_author_list_queryset()

        ids = list(queryset.values_list("id", flat=True))

        assert ids == [new.id, old.id]

    def test_get_author_list_queryset_only_loads_requested_fields(self, author_factory, list_deferred_fields):
        author = author_factory(name="Author 1", about="About Author 1", biography="Biography Author 1", avatar=None)
        deferred_fields = list_deferred_fields(author.id)

        assert "id" not in deferred_fields
        assert "name" not in deferred_fields
        assert "avatar" not in deferred_fields
        assert deferred_fields == {"about", "biography", "created_at", "modified_at"}


@pytest.mark.django_db
class TestGetAuthorDetailQueryset:

    def test_get_author_detail_queryset_returns_author(self, author_factory):
        author = author_factory(name="Author 1")
        author_from_db = get_public_author_detail_queryset().get(id=author.id)

        assert author_from_db.id == author.id
        assert author_from_db.name == author.name

    def test_get_author_detail_queryset_only_loads_requested_fields(self, author_factory, detail_deferred_fields):
        author = author_factory(name="Author 1", about="About Author 1", biography="Biography Author 1", avatar=None)
        deferred_fields = detail_deferred_fields(author.id)

        assert "id" not in deferred_fields
        assert "name" not in deferred_fields
        assert "about" not in deferred_fields
        assert "biography" not in deferred_fields
        assert "avatar" not in deferred_fields
        assert deferred_fields == {"created_at", "modified_at"}
