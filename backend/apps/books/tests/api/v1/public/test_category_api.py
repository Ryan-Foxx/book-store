from datetime import timedelta

import pytest
from apps.books.models import Category
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestCategoryListApi:

    def test_get_category_list(self, api_client, public_category_list_url):
        response = api_client.get(public_category_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_category_list_returns_categories(self, api_client, category_factory, public_category_list_url):
        category_factory(title="Category 1")
        category_factory(title="Category 2")

        response = api_client.get(public_category_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_category_list_expected_fields(self, api_client, public_category_list_url, category_factory):
        category = category_factory(title="Management")

        response = api_client.get(public_category_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == category.id
        assert set(results[0].keys()) == {"id", "title"}
        assert results[0]["title"] == "Management"

    def test_get_category_list_ordered_by_created_at_desc(self, api_client, category_factory, public_category_list_url):
        now = timezone.now()

        old = category_factory(title="Old Category")
        Category.objects.filter(id=old.id).update(created_at=now - timedelta(days=2))

        new = category_factory(title="New Category")
        Category.objects.filter(id=new.id).update(created_at=now)

        response = api_client.get(public_category_list_url)

        results = response.data["results"]

        ids = [a["id"] for a in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [new.id, old.id]

    def test_get_category_list_search_by_title(self, api_client, category_factory, public_category_list_url):
        target = category_factory(title="Management")

        category_factory(title="Personal Development")

        response = api_client.get(public_category_list_url, {"search": "Manage"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["title"] == "Management"

    def test_get_category_list_search_is_case_insensitive(self, api_client, category_factory, public_category_list_url):
        target = category_factory(title="Management")

        category_factory(title="Personal Development")

        response = api_client.get(public_category_list_url, {"search": "mAnAge"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["title"] == "Management"

    def test_get_category_list_search_returns_empty_list_when_no_match(
        self, api_client, category_factory, public_category_list_url
    ):
        category_factory(title="Management")
        category_factory(title="Personal Development")

        response = api_client.get(public_category_list_url, {"search": "Tesla"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results == []

    def test_get_category_list_pagination_structure(self, api_client, category_factory, public_category_list_url):
        category_factory(title="Category 1")
        category_factory(title="Category 2")

        response = api_client.get(public_category_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {
            "count",
            "pages",
            "current_page",
            "page_size",
            "next",
            "previous",
            "results",
        }

        assert response.data["count"] == 2
        assert response.data["pages"] == 1
        assert response.data["current_page"] == 1
        assert response.data["page_size"] == 20
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 2

    def test_get_category_list_default_page_size(self, api_client, category_factory, public_category_list_url):
        for i in range(30):
            category_factory(title=f"Category {i}")

        response = api_client.get(public_category_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_category_list_custom_page_size(self, api_client, category_factory, public_category_list_url):
        for i in range(20):
            category_factory(title=f"Category {i}")

        response = api_client.get(f"{public_category_list_url}?page_size=10")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 20
        assert response.data["pages"] == 2

    def test_get_category_list_page_size_respects_max_limit(
        self, api_client, category_factory, public_category_list_url
    ):
        for i in range(60):
            category_factory(title=f"Category {i}")

        response = api_client.get(f"{public_category_list_url}?page_size=100")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_category_list_next_link_exists_on_first_page(
        self, api_client, category_factory, public_category_list_url
    ):
        for i in range(30):
            category_factory(title=f"Category {i}")

        response = api_client.get(f"{public_category_list_url}?page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_category_list_previous_link_exists_on_second_page(
        self, api_client, category_factory, public_category_list_url
    ):
        for i in range(30):
            category_factory(title=f"Category {i}")

        response = api_client.get(f"{public_category_list_url}?page=2&page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    def test_category_list_post_not_allowed(self, api_client, public_category_list_url):

        payload = {"title": "Management"}

        response = api_client.post(public_category_list_url, payload)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert not Category.objects.filter(title="Management").exists()


@pytest.mark.django_db
class TestCategoryDetailApi:

    def test_get_category_detail(self, api_client, category_factory, public_category_detail_url):
        category = category_factory(title="Management")

        response = api_client.get(public_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_get_category_detail_returns_category(self, api_client, category_factory, public_category_detail_url):
        category = category_factory(title="Management")
        response = api_client.get(public_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == category.id
        assert response.data["title"] == category.title

    def test_get_category_detail_expected_fields(self, api_client, category_factory, public_category_detail_url):
        category = category_factory(title="Management")
        response = api_client.get(public_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {"id", "title", "description"}
        assert response.data["title"] == "Management"

    def test_get_category_detail_not_found(self, api_client, public_category_detail_url):
        response = api_client.get(public_category_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_category_detail_put_not_allowed(self, api_client, category_factory, public_category_detail_url):
        category = category_factory(title="Category 1")

        payload = {"title": "Updated category"}

        response = api_client.put(public_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert category.title == "Category 1"

    def test_category_detail_patch_not_allowed(self, api_client, category_factory, public_category_detail_url):
        category = category_factory(title="Category 1")

        payload = {"title": "Updated category"}

        response = api_client.patch(public_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert category.title == "Category 1"

    def test_category_detail_delete_not_allowed(self, api_client, category_factory, public_category_detail_url):
        category = category_factory(title="Category 1")
        response = api_client.delete(public_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert Category.objects.filter(id=category.id).exists()
