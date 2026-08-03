import pytest
from apps.books.api.v1.public.serializers.author_serializers import (
    AuthorDetailSerializer,
    AuthorListSerializer,
)


@pytest.fixture
def author_data():
    return {"name": "New Author", "about": "About text", "biography": "Biography text"}


@pytest.mark.django_db
class TestAuthorListSerializer:

    def test_author_list_serializer_expected_fields(self):
        serializer = AuthorListSerializer()

        assert set(serializer.fields.keys()) == {"id", "name", "avatar"}

    def test_author_list_serializer_returns_expected_data(self, author_factory):
        author = author_factory(name="Author 1")
        data = AuthorListSerializer(author).data

        assert data["id"] == author.id
        assert data["name"] == author.name
        assert "avatar" in data
        assert set(data.keys()) == {"id", "name", "avatar"}

    def test_author_list_serializer_avatar_can_be_null(self, author_factory):
        author = author_factory(name="No Avatar Author", avatar=None)
        data = AuthorListSerializer(author).data

        assert data["avatar"] is None


@pytest.mark.django_db
class TestAuthorDetailSerializer:

    def test_author_detail_serializer_expected_fields(self):
        serializer = AuthorDetailSerializer()

        assert set(serializer.fields.keys()) == {"id", "name", "avatar", "about", "biography"}

    def test_author_detail_serializer_returns_expected_data(self, author_factory):
        author = author_factory(name="Author 1", about="About Author 1", biography="Biography Author 1")
        data = AuthorDetailSerializer(author).data

        assert data["id"] == author.id
        assert data["name"] == author.name
        assert data["about"] == author.about
        assert data["biography"] == author.biography
        assert "avatar" in data
        assert set(data.keys()) == {"id", "name", "avatar", "about", "biography"}

    def test_author_detail_serializer_requires_name(self):
        serializer = AuthorDetailSerializer(data={"about": "About text", "biography": "Biography text"})

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_author_detail_serializer_validates_unique_name(self, author_factory, author_data):
        author = author_factory(name="Author 1", about="About Author 1", biography="Biography Author 1")
        serializer = AuthorDetailSerializer(data={**author_data, "name": author.name})

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_author_detail_serializer_allows_blank_about_and_biography(self, author_data):
        serializer = AuthorDetailSerializer(data={**author_data, "about": "", "biography": ""})

        assert serializer.is_valid()
        assert serializer.errors == {}
