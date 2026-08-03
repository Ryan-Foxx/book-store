import pytest
from rest_framework import status


@pytest.mark.django_db
class TestAuthorListViewSet:
    def test_author_list_returns_paginated_authors(self, api_client, author_factory, public_author_list_url):
        author_factory(name="Alice")
        author_factory(name="Bob")

        response = api_client.get(public_author_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert "count" in response.data
        assert "pages" in response.data
        assert "current_page" in response.data
        assert "page_size" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

        assert response.data["count"] == 2
        assert len(response.data["results"]) == 2

        first_item = response.data["results"][0]
        assert set(first_item.keys()) == {"id", "name", "avatar"}

    def test_author_list_orders_by_newest_first(self, api_client, author_factory, public_author_list_url):
        old_author = author_factory(name="Old Author")
        new_author = author_factory(name="New Author")

        response = api_client.get(public_author_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["name"] == new_author.name
        assert response.data["results"][1]["name"] == old_author.name

    def test_author_search_filters_by_name(self, api_client, author_factory, public_author_list_url):
        author_factory(name="Ali Reza")
        author_factory(name="Sara")
        author_factory(name="Mohammad Ali")

        response = api_client.get(public_author_list_url, {"search": "ali"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        names = [item["name"] for item in response.data["results"]]
        assert "Ali Reza" in names
        assert "Mohammad Ali" in names
        assert "Sara" not in names


@pytest.mark.django_db
class TestAuthorDetailViewSet:

    def test_author_detail_returns_full_author_data(self, api_client, author_factory, public_author_detail_url):
        author = author_factory(name="Alice", about="About Alice", biography="Biography Alice")

        response = api_client.get(public_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {"id", "name", "avatar", "about", "biography"}
        assert response.data["name"] == "Alice"
        assert response.data["about"] == "About Alice"
        assert response.data["biography"] == "Biography Alice"

    def test_author_detail_not_found_returns_404(self, api_client, public_author_detail_url):
        response = api_client.get(public_author_detail_url(999))

        assert response.status_code == status.HTTP_404_NOT_FOUND
