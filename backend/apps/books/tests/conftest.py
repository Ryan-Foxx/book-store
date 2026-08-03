import pytest
from apps.books.models import Author
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def author_factory(db):
    def create_author(**kwargs):
        return Author.objects.create(
            name=kwargs.get("name", "John Doe"),
            about=kwargs.get("about", "About John"),
            biography=kwargs.get("biography", "Biography John"),
            avatar=kwargs.get("avatar", None),
        )

    return create_author


@pytest.fixture
def public_author_list_url():
    return reverse("public-author-list")


@pytest.fixture
def public_author_detail_url():
    def url(author_id):
        return reverse("public-author-detail", kwargs={"pk": author_id})

    return url
