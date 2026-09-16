from datetime import timedelta

import pytest
from apps.books.models import Category
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestCategoryListApi:

    def test_owner_can_get_category_list(self, owner_client, admin_category_list_url):
        response = owner_client.get(admin_category_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_category_list(self, admin_client, admin_category_list_url):
        response = admin_client.get(admin_category_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_category_list(self, customer_client, admin_category_list_url):
        response = customer_client.get(admin_category_list_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_category_list(self, api_client, admin_category_list_url):
        response = api_client.get(admin_category_list_url)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_owner_get_category_list_returns_categories(self, owner_client, category_factory, admin_category_list_url):
        category_factory(title="Category 1")
        category_factory(title="Category 2")

        response = owner_client.get(admin_category_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_admin_get_category_list_returns_categories(self, admin_client, category_factory, admin_category_list_url):
        category_factory(title="Category 1")
        category_factory(title="Category 2")

        response = admin_client.get(admin_category_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_category_list_expected_fields(self, owner_client, category_factory, admin_category_list_url):
        category = category_factory(title="Management")

        response = owner_client.get(admin_category_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == category.id
        assert set(results[0].keys()) == {"id", "title", "description", "created_at", "modified_at"}
        assert results[0]["title"] == "Management"

    def test_get_category_list_ordered_by_modified_at_desc(
        self, owner_client, category_factory, admin_category_list_url
    ):
        now = timezone.now()

        old = category_factory(title="Old Category")
        Category.objects.filter(id=old.id).update(modified_at=now - timedelta(days=2))

        new = category_factory(title="New Category")
        Category.objects.filter(id=new.id).update(modified_at=now)

        response = owner_client.get(admin_category_list_url)

        results = response.data["results"]
        ids = [category["id"] for category in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [new.id, old.id]

    def test_get_category_list_search_by_title(self, owner_client, category_factory, admin_category_list_url):
        target = category_factory(title="Management")
        category_factory(title="Personal Development")

        response = owner_client.get(admin_category_list_url, {"search": "Manage"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["title"] == "Management"

    def test_get_category_list_search_is_case_insensitive(
        self, owner_client, category_factory, admin_category_list_url
    ):
        target = category_factory(title="Management")
        category_factory(title="Personal Development")

        response = owner_client.get(admin_category_list_url, {"search": "ManAge"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["title"] == "Management"

    def test_get_category_list_search_returns_empty_list_when_no_match(
        self, owner_client, category_factory, admin_category_list_url
    ):
        category_factory(title="Management")
        category_factory(title="Personal Development")

        response = owner_client.get(admin_category_list_url, {"search": "Tesla"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results == []

    def test_get_category_list_ordering_by_id(self, owner_client, category_factory, admin_category_list_url):
        first = category_factory(title="Category 1")
        second = category_factory(title="Category 2")
        third = category_factory(title="Category 3")

        response = owner_client.get(admin_category_list_url, {"ordering": "id"})

        results = response.data["results"]
        ids = [category["id"] for category in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [first.id, second.id, third.id]

    def test_get_category_list_ordering_by_id_desc(self, owner_client, category_factory, admin_category_list_url):
        first = category_factory(title="Category 1")
        second = category_factory(title="Category 2")
        third = category_factory(title="Category 3")

        response = owner_client.get(admin_category_list_url, {"ordering": "-id"})

        results = response.data["results"]
        ids = [category["id"] for category in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [third.id, second.id, first.id]

    def test_get_category_list_ordering_by_created_at(self, owner_client, category_factory, admin_category_list_url):
        first = category_factory(title="Category 1")
        second = category_factory(title="Category 2")

        response = owner_client.get(admin_category_list_url, {"ordering": "created_at"})

        results = response.data["results"]
        ids = [category["id"] for category in results]

        assert response.status_code == status.HTTP_200_OK
        assert set(ids) == {first.id, second.id}

    def test_get_category_list_ordering_by_modified_at(self, owner_client, category_factory, admin_category_list_url):
        first = category_factory(title="Category 1")
        second = category_factory(title="Category 2")

        response = owner_client.get(admin_category_list_url, {"ordering": "-modified_at"})

        results = response.data["results"]
        ids = [category["id"] for category in results]

        assert response.status_code == status.HTTP_200_OK
        assert set(ids) == {first.id, second.id}

    def test_get_category_list_pagination_structure(self, owner_client, category_factory, admin_category_list_url):
        category_factory(title="Category 1")
        category_factory(title="Category 2")

        response = owner_client.get(admin_category_list_url)

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

    def test_get_category_list_default_page_size(self, owner_client, category_factory, admin_category_list_url):
        for i in range(30):
            category_factory(title=f"Category {i}")

        response = owner_client.get(admin_category_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_category_list_custom_page_size(self, owner_client, category_factory, admin_category_list_url):
        for i in range(20):
            category_factory(title=f"Category {i}")

        response = owner_client.get(f"{admin_category_list_url}?page_size=10")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 20
        assert response.data["pages"] == 2

    def test_get_category_list_page_size_respects_max_limit(
        self, owner_client, category_factory, admin_category_list_url
    ):
        for i in range(60):
            category_factory(title=f"Category {i}")

        response = owner_client.get(f"{admin_category_list_url}?page_size=100")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_category_list_next_link_exists_on_first_page(
        self, owner_client, category_factory, admin_category_list_url
    ):
        for i in range(30):
            category_factory(title=f"Category {i}")

        response = owner_client.get(f"{admin_category_list_url}?page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_category_list_previous_link_exists_on_second_page(
        self, owner_client, category_factory, admin_category_list_url
    ):
        for i in range(30):
            category_factory(title=f"Category {i}")

        response = owner_client.get(f"{admin_category_list_url}?page=2&page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    def test_owner_can_create_category(self, owner_client, admin_category_list_url):

        payload = {"title": "Management"}

        response = owner_client.post(admin_category_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(title="Management").exists()

    def test_admin_can_create_category(self, admin_client, admin_category_list_url):

        payload = {"title": "Management"}

        response = admin_client.post(admin_category_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(title="Management").exists()

    def test_customer_cannot_create_category(self, customer_client, admin_category_list_url):

        payload = {"title": "Management"}

        response = customer_client.post(admin_category_list_url, payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Category.objects.filter(title="Management").exists()

    def test_category_title_is_required(self, owner_client, admin_category_list_url):
        payload = {"description": "Management description"}

        response = owner_client.post(admin_category_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_category_title_must_be_unique(self, owner_client, category_factory, admin_category_list_url):
        category_factory(title="Management")

        payload = {"title": "Management"}

        response = owner_client.post(admin_category_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data


@pytest.mark.django_db
class TestCategoryDetailApi:

    def test_owner_can_get_category_detail(self, owner_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = owner_client.get(admin_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_category_detail(self, admin_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = admin_client.get(admin_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_category_detail(self, customer_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = customer_client.get(admin_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_category_detail(self, api_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = api_client.get(admin_category_detail_url(category.pk))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_category_detail_returns_category(self, owner_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = owner_client.get(admin_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == category.id
        assert response.data["title"] == category.title

    def test_get_category_detail_expected_fields(self, owner_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = owner_client.get(admin_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {"id", "title", "description", "created_at", "modified_at"}
        assert response.data["title"] == "Management"

    def test_get_category_detail_not_found(self, owner_client, admin_category_detail_url):
        response = owner_client.get(admin_category_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_owner_can_patch_category(self, owner_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management", description="Management description")

        payload = {"title": "Updated title"}

        response = owner_client.patch(admin_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert category.title == "Updated title"

    def test_admin_can_patch_category(self, admin_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management", description="Management description")

        payload = {"title": "Updated title"}

        response = admin_client.patch(admin_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert category.title == "Updated title"

    def test_customer_cannot_patch_category(self, customer_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management", description="Management description")

        payload = {"title": "Updated title"}

        response = customer_client.patch(admin_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert category.title == "Management"

    def test_owner_can_put_category(self, owner_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Old Category", description="Old description")

        payload = {"title": "Updated Category", "description": "Updated description"}

        response = owner_client.put(admin_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert category.title == "Updated Category"
        assert category.description == "Updated description"

    def test_admin_can_put_category(self, admin_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Old Category", description="Old description")

        payload = {"title": "Updated Category", "description": "Updated description"}

        response = admin_client.put(admin_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert category.title == "Updated Category"
        assert category.description == "Updated description"

    def test_customer_cannot_put_category(self, customer_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Old Category", description="Old description")

        payload = {"title": "Updated Category", "description": "Updated description"}

        response = customer_client.put(admin_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert category.title == "Old Category"
        assert category.description == "Old description"

    def test_owner_can_delete_category(self, owner_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = owner_client.delete(admin_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(id=category.id).exists()

    def test_admin_cannot_delete_category(self, admin_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = admin_client.delete(admin_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Category.objects.filter(id=category.id).exists()

    def test_customer_cannot_delete_category(self, customer_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management")

        response = customer_client.delete(admin_category_detail_url(category.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Category.objects.filter(id=category.id).exists()

    def test_category_title_is_required_on_put(self, owner_client, category_factory, admin_category_detail_url):
        category = category_factory(title="Management", description="Management description")

        payload = {"description": "Updated description"}

        response = owner_client.put(admin_category_detail_url(category.pk), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_category_title_must_be_unique_on_put(self, owner_client, category_factory, admin_category_detail_url):
        category_factory(title="Management", description="Management description")
        second_category = category_factory(title="Personal Development", description="Personal Development description")

        payload = {"title": "Management", "description": "Management description"}

        response = owner_client.put(admin_category_detail_url(second_category.pk), payload)

        second_category.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
        assert second_category.title == "Personal Development"

    def test_category_title_must_be_unique_on_patch(self, owner_client, category_factory, admin_category_detail_url):
        category_factory(title="Management", description="Management description")
        second_category = category_factory(title="Personal Development", description="Personal Development description")

        payload = {"title": "Management"}

        response = owner_client.patch(admin_category_detail_url(second_category.pk), payload)

        second_category.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
        assert second_category.title == "Personal Development"

    def test_category_read_only_fields_are_ignored_on_put(
        self, owner_client, category_factory, admin_category_detail_url
    ):
        category = category_factory(title="Management", description="Management description")

        old_id = category.id
        old_created_at = category.created_at

        payload = {
            "id": 999999,
            "title": "Updated category",
            "description": "Updated description",
            "created_at": "2000-01-01T00:00:00Z",
            "modified_at": "2000-01-01T00:00:00Z",
        }

        response = owner_client.put(admin_category_detail_url(category.pk), payload)

        category.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert category.id == old_id
        assert category.created_at == old_created_at
        assert category.title == "Updated category"
        assert category.description == "Updated description"
