from datetime import timedelta

import pytest
from apps.books.models import Language
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestLanguageListApi:

    def test_owner_can_get_language_list(self, owner_client, admin_language_list_url):
        response = owner_client.get(admin_language_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_language_list(self, admin_client, admin_language_list_url):
        response = admin_client.get(admin_language_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_language_list(self, customer_client, admin_language_list_url):
        response = customer_client.get(admin_language_list_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_language_list(self, api_client, admin_language_list_url):
        response = api_client.get(admin_language_list_url)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_owner_get_language_list_returns_language(self, owner_client, language_factory, admin_language_list_url):
        language_factory(name="Language 1")
        language_factory(name="Language 2")

        response = owner_client.get(admin_language_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_admin_get_language_list_returns_language(self, admin_client, language_factory, admin_language_list_url):
        language_factory(name="Language 1")
        language_factory(name="Language 2")

        response = admin_client.get(admin_language_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_language_list_expected_fields(self, owner_client, language_factory, admin_language_list_url):
        language = language_factory(name="English")

        response = owner_client.get(admin_language_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == language.id
        assert set(results[0].keys()) == {"id", "name", "created_at", "modified_at"}
        assert results[0]["name"] == "English"

    def test_get_language_list_ordered_by_modified_at_desc(
        self, owner_client, language_factory, admin_language_list_url
    ):
        now = timezone.now()

        old = language_factory(name="Old Language")
        Language.objects.filter(id=old.id).update(modified_at=now - timedelta(days=2))

        new = language_factory(name="New Language")
        Language.objects.filter(id=new.id).update(modified_at=now)

        response = owner_client.get(admin_language_list_url)

        results = response.data["results"]
        ids = [language["id"] for language in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [new.id, old.id]

    def test_get_language_list_search_by_name(self, owner_client, language_factory, admin_language_list_url):
        target = language_factory(name="English")
        language_factory(name="Arabic")

        response = owner_client.get(admin_language_list_url, {"search": "Eng"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "English"

    def test_get_language_list_search_is_case_insensitive(
        self, owner_client, language_factory, admin_language_list_url
    ):
        target = language_factory(name="English")
        language_factory(name="Arabic")

        response = owner_client.get(admin_language_list_url, {"search": "EnG"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "English"

    def test_get_language_list_search_returns_empty_list_when_no_match(
        self, owner_client, language_factory, admin_language_list_url
    ):
        language_factory(name="English")
        language_factory(name="Arabic")

        response = owner_client.get(admin_language_list_url, {"search": "Tesla"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results == []

    def test_get_language_list_ordering_by_id(self, owner_client, language_factory, admin_language_list_url):
        first = language_factory(name="Language 1")
        second = language_factory(name="Language 2")
        third = language_factory(name="Language 3")

        response = owner_client.get(admin_language_list_url, {"ordering": "id"})

        results = response.data["results"]
        ids = [language["id"] for language in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [first.id, second.id, third.id]

    def test_get_language_list_ordering_by_id_desc(self, owner_client, language_factory, admin_language_list_url):
        first = language_factory(name="Language 1")
        second = language_factory(name="Language 2")
        third = language_factory(name="Language 3")

        response = owner_client.get(admin_language_list_url, {"ordering": "-id"})

        results = response.data["results"]
        ids = [language["id"] for language in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [third.id, second.id, first.id]

    def test_get_language_list_ordering_by_created_at(self, owner_client, language_factory, admin_language_list_url):
        first = language_factory(name="Language 1")
        second = language_factory(name="Language 2")

        response = owner_client.get(admin_language_list_url, {"ordering": "created_at"})

        results = response.data["results"]
        ids = [language["id"] for language in results]

        assert response.status_code == status.HTTP_200_OK
        assert set(ids) == {first.id, second.id}

    def test_get_language_list_ordering_by_modified_at(self, owner_client, language_factory, admin_language_list_url):
        first = language_factory(name="Language 1")
        second = language_factory(name="Language 2")

        response = owner_client.get(admin_language_list_url, {"ordering": "-modified_at"})

        results = response.data["results"]
        ids = [language["id"] for language in results]

        assert response.status_code == status.HTTP_200_OK
        assert set(ids) == {first.id, second.id}

    def test_get_language_list_pagination_structure(self, owner_client, language_factory, admin_language_list_url):
        language_factory(name="Language 1")
        language_factory(name="Language 2")

        response = owner_client.get(admin_language_list_url)

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

    def test_get_language_list_default_page_size(self, owner_client, language_factory, admin_language_list_url):
        for i in range(30):
            language_factory(name=f"Language {i}")

        response = owner_client.get(admin_language_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_language_list_custom_page_size(self, owner_client, language_factory, admin_language_list_url):
        for i in range(20):
            language_factory(name=f"Language {i}")

        response = owner_client.get(f"{admin_language_list_url}?page_size=10")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 20
        assert response.data["pages"] == 2

    def test_get_language_list_page_size_respects_max_limit(
        self, owner_client, language_factory, admin_language_list_url
    ):
        for i in range(60):
            language_factory(name=f"Language {i}")

        response = owner_client.get(f"{admin_language_list_url}?page_size=100")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_language_list_next_link_exists_on_first_page(
        self, owner_client, language_factory, admin_language_list_url
    ):
        for i in range(30):
            language_factory(name=f"Language {i}")

        response = owner_client.get(f"{admin_language_list_url}?page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_language_list_previous_link_exists_on_second_page(
        self, owner_client, language_factory, admin_language_list_url
    ):
        for i in range(30):
            language_factory(name=f"Language {i}")

        response = owner_client.get(f"{admin_language_list_url}?page=2&page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    def test_owner_can_create_language(self, owner_client, admin_language_list_url):

        payload = {"name": "English"}

        response = owner_client.post(admin_language_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Language.objects.filter(name="English").exists()

    def test_admin_can_create_language(self, admin_client, admin_language_list_url):

        payload = {"name": "English"}

        response = admin_client.post(admin_language_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Language.objects.filter(name="English").exists()

    def test_customer_cannot_create_language(self, customer_client, admin_language_list_url):

        payload = {"name": "English"}

        response = customer_client.post(admin_language_list_url, payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Language.objects.filter(name="English").exists()

    def test_language_name_is_required(self, owner_client, admin_language_list_url):
        payload = {}

        response = owner_client.post(admin_language_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_language_name_must_be_unique(self, owner_client, language_factory, admin_language_list_url):
        language_factory(name="English")

        payload = {"name": "English"}

        response = owner_client.post(admin_language_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data


@pytest.mark.django_db
class TestLanguageDetailApi:

    def test_owner_can_get_language_detail(self, owner_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = owner_client.get(admin_language_detail_url(language.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_language_detail(self, admin_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = admin_client.get(admin_language_detail_url(language.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_language_detail(self, customer_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = customer_client.get(admin_language_detail_url(language.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_language_detail(self, api_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = api_client.get(admin_language_detail_url(language.pk))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_language_detail_returns_language(self, owner_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = owner_client.get(admin_language_detail_url(language.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == language.id
        assert response.data["name"] == language.name

    def test_get_language_detail_expected_fields(self, owner_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = owner_client.get(admin_language_detail_url(language.pk))

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {"id", "name", "created_at", "modified_at"}
        assert response.data["name"] == "English"

    def test_get_language_detail_not_found(self, owner_client, admin_language_detail_url):
        response = owner_client.get(admin_language_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_owner_can_patch_language(self, owner_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        payload = {"name": "Updated name"}

        response = owner_client.patch(admin_language_detail_url(language.pk), payload)

        language.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert language.name == "Updated name"

    def test_admin_can_patch_language(self, admin_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        payload = {"name": "Updated name"}

        response = admin_client.patch(admin_language_detail_url(language.pk), payload)

        language.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert language.name == "Updated name"

    def test_customer_cannot_patch_language(self, customer_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        payload = {"name": "Updated name"}

        response = customer_client.patch(admin_language_detail_url(language.pk), payload)

        language.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert language.name == "English"

    def test_owner_can_put_language(self, owner_client, language_factory, admin_language_detail_url):
        language = language_factory(name="Old English")

        payload = {"name": "Updated language"}

        response = owner_client.put(admin_language_detail_url(language.pk), payload)

        language.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert language.name == "Updated language"

    def test_admin_can_put_language(self, admin_client, language_factory, admin_language_detail_url):
        language = language_factory(name="Old English")

        payload = {"name": "Updated language"}

        response = admin_client.put(admin_language_detail_url(language.pk), payload)

        language.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert language.name == "Updated language"

    def test_customer_cannot_put_language(self, customer_client, language_factory, admin_language_detail_url):
        language = language_factory(name="Old English")

        payload = {"name": "Updated language"}

        response = customer_client.put(admin_language_detail_url(language.pk), payload)

        language.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert language.name == "Old English"

    def test_owner_can_delete_language(self, owner_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = owner_client.delete(admin_language_detail_url(language.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Language.objects.filter(id=language.id).exists()

    def test_admin_cannot_delete_language(self, admin_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = admin_client.delete(admin_language_detail_url(language.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Language.objects.filter(id=language.id).exists()

    def test_customer_cannot_delete_language(self, customer_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        response = customer_client.delete(admin_language_detail_url(language.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Language.objects.filter(id=language.id).exists()

    def test_language_name_is_required_on_put(self, owner_client, language_factory, admin_language_detail_url):
        language = language_factory(name="English")

        payload = {}

        response = owner_client.put(admin_language_detail_url(language.pk), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_language_name_must_be_unique_on_put(self, owner_client, language_factory, admin_language_detail_url):
        language_factory(name="English")
        second_language = language_factory(name="Arabic")

        payload = {"name": "English"}

        response = owner_client.put(admin_language_detail_url(second_language.pk), payload)

        second_language.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert second_language.name == "Arabic"

    def test_language_name_must_be_unique_on_patch(self, owner_client, language_factory, admin_language_detail_url):
        language_factory(name="English")
        second_language = language_factory(name="Arabic")

        payload = {"name": "English"}

        response = owner_client.patch(admin_language_detail_url(second_language.pk), payload)

        second_language.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert second_language.name == "Arabic"

    def test_language_read_only_fields_are_ignored_on_put(
        self, owner_client, language_factory, admin_language_detail_url
    ):
        language = language_factory(name="English")

        old_id = language.id
        old_created_at = language.created_at

        payload = {
            "id": 999999,
            "name": "Updated language",
            "created_at": "2000-01-01T00:00:00Z",
            "modified_at": "2000-01-01T00:00:00Z",
        }

        response = owner_client.put(admin_language_detail_url(language.pk), payload)

        language.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert language.id == old_id
        assert language.created_at == old_created_at
        assert language.name == "Updated language"
