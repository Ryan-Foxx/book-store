from datetime import date, timedelta

import pytest
from apps.books.models import Translator
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestTranslatorListApi:

    def test_owner_can_get_translator_list(self, owner_client, admin_translator_list_url):
        response = owner_client.get(admin_translator_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_translator_list(self, admin_client, admin_translator_list_url):
        response = admin_client.get(admin_translator_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_translator_list(self, customer_client, admin_translator_list_url):
        response = customer_client.get(admin_translator_list_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_translator_list(self, api_client, admin_translator_list_url):
        response = api_client.get(admin_translator_list_url)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_owner_get_translator_list_returns_translators(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        translator_factory(name="Translator 1")
        translator_factory(name="Translator 2")

        response = owner_client.get(admin_translator_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_admin_get_translator_list_returns_translators(
        self, admin_client, translator_factory, admin_translator_list_url
    ):
        translator_factory(name="Translator 1")
        translator_factory(name="Translator 2")

        response = admin_client.get(admin_translator_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_translator_list_expected_fields(self, owner_client, translator_factory, admin_translator_list_url):
        translator = translator_factory(name="Robert Johnson")

        response = owner_client.get(admin_translator_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == translator.id
        assert set(results[0].keys()) == {"id", "name", "avatar", "about", "created_at", "modified_at"}
        assert results[0]["name"] == "Robert Johnson"

    def test_get_translator_list_ordered_by_modified_at_desc(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        now = timezone.now()

        old = translator_factory(name="Old Translator")
        Translator.objects.filter(id=old.id).update(modified_at=now - timedelta(days=2))

        new = translator_factory(name="New Translator")
        Translator.objects.filter(id=new.id).update(modified_at=now)

        response = owner_client.get(admin_translator_list_url)

        results = response.data["results"]
        ids = [translator["id"] for translator in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [new.id, old.id]

    def test_get_translator_list_search_by_name(self, owner_client, translator_factory, admin_translator_list_url):
        target = translator_factory(name="Robert Johnson")
        translator_factory(name="Jack Anderson")

        response = owner_client.get(admin_translator_list_url, {"search": "Robe"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "Robert Johnson"

    def test_get_translator_list_search_is_case_insensitive(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        target = translator_factory(name="Robert Johnson")
        translator_factory(name="Jack Anderson")

        response = owner_client.get(admin_translator_list_url, {"search": "RoB"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "Robert Johnson"

    def test_get_translator_list_search_returns_empty_list_when_no_match(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        translator_factory(name="Robert Johnson")
        translator_factory(name="Jack Anderson")

        response = owner_client.get(admin_translator_list_url, {"search": "Tesla"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results == []

    def test_get_translator_list_ordering_by_id(self, owner_client, translator_factory, admin_translator_list_url):
        first = translator_factory(name="Translator 1")
        second = translator_factory(name="Translator 2")
        third = translator_factory(name="Translator 3")

        response = owner_client.get(admin_translator_list_url, {"ordering": "id"})

        results = response.data["results"]
        ids = [translator["id"] for translator in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [first.id, second.id, third.id]

    def test_get_translator_list_ordering_by_id_desc(self, owner_client, translator_factory, admin_translator_list_url):
        first = translator_factory(name="Translator 1")
        second = translator_factory(name="Translator 2")
        third = translator_factory(name="Translator 3")

        response = owner_client.get(admin_translator_list_url, {"ordering": "-id"})

        results = response.data["results"]
        ids = [translator["id"] for translator in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [third.id, second.id, first.id]

    def test_get_translator_list_ordering_by_created_at(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        first = translator_factory(name="Translator 1")
        second = translator_factory(name="Translator 2")

        response = owner_client.get(admin_translator_list_url, {"ordering": "created_at"})

        results = response.data["results"]
        ids = [translator["id"] for translator in results]

        assert response.status_code == status.HTTP_200_OK
        assert set(ids) == {first.id, second.id}

    def test_get_translator_list_ordering_by_modified_at(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        first = translator_factory(name="Translator 1")
        second = translator_factory(name="Translator 2")

        response = owner_client.get(admin_translator_list_url, {"ordering": "-modified_at"})

        results = response.data["results"]
        ids = [translator["id"] for translator in results]

        assert response.status_code == status.HTTP_200_OK
        assert set(ids) == {first.id, second.id}

    def test_get_translator_list_pagination_structure(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        translator_factory(name="Translator 1")
        translator_factory(name="Translator 2")

        response = owner_client.get(admin_translator_list_url)

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

    def test_get_translator_list_default_page_size(self, owner_client, translator_factory, admin_translator_list_url):
        for i in range(30):
            translator_factory(name=f"Translator {i}")

        response = owner_client.get(admin_translator_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_translator_list_custom_page_size(self, owner_client, translator_factory, admin_translator_list_url):
        for i in range(20):
            translator_factory(name=f"Translator {i}")

        response = owner_client.get(f"{admin_translator_list_url}?page_size=10")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 20
        assert response.data["pages"] == 2

    def test_get_translator_list_page_size_respects_max_limit(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        for i in range(60):
            translator_factory(name=f"Translator {i}")

        response = owner_client.get(f"{admin_translator_list_url}?page_size=100")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_translator_list_next_link_exists_on_first_page(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        for i in range(30):
            translator_factory(name=f"Translator {i}")

        response = owner_client.get(f"{admin_translator_list_url}?page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_translator_list_previous_link_exists_on_second_page(
        self, owner_client, translator_factory, admin_translator_list_url
    ):
        for i in range(30):
            translator_factory(name=f"Translator {i}")

        response = owner_client.get(f"{admin_translator_list_url}?page=2&page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    def test_owner_can_create_translator(self, owner_client, admin_translator_list_url):

        payload = {"name": "Robert Johnson"}

        response = owner_client.post(admin_translator_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Translator.objects.filter(name="Robert Johnson").exists()

    def test_admin_can_create_translator(self, admin_client, admin_translator_list_url):

        payload = {"name": "Robert Johnson"}

        response = admin_client.post(admin_translator_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Translator.objects.filter(name="Robert Johnson").exists()

    def test_customer_cannot_create_translator(self, customer_client, admin_translator_list_url):

        payload = {"name": "Robert Johnson"}

        response = customer_client.post(admin_translator_list_url, payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Translator.objects.filter(name="Robert Johnson").exists()

    def test_translator_name_is_required(self, owner_client, admin_translator_list_url):
        payload = {"about": "Robert is very good! person"}

        response = owner_client.post(admin_translator_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_translator_name_must_be_unique(self, owner_client, translator_factory, admin_translator_list_url):
        translator_factory(name="Robert Johnson")

        payload = {"name": "Robert Johnson"}

        response = owner_client.post(admin_translator_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data


@pytest.mark.django_db
class TestTranslatorDetailApi:

    def test_owner_can_get_translator_detail(self, owner_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson")

        response = owner_client.get(admin_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_translator_detail(self, admin_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson")

        response = admin_client.get(admin_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_translator_detail(
        self, customer_client, translator_factory, admin_translator_detail_url
    ):
        translator = translator_factory(name="Robert Johnson")

        response = customer_client.get(admin_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_translator_detail(self, api_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson")

        response = api_client.get(admin_translator_detail_url(translator.pk))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_translator_detail_returns_translator(
        self, owner_client, translator_factory, admin_translator_detail_url
    ):
        translator = translator_factory(name="Robert Johnson")

        response = owner_client.get(admin_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == translator.id
        assert response.data["name"] == translator.name

    def test_get_translator_detail_expected_fields(self, owner_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson")

        response = owner_client.get(admin_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {"id", "name", "avatar", "about", "created_at", "modified_at"}
        assert response.data["name"] == "Robert Johnson"

    def test_get_translator_detail_not_found(self, owner_client, admin_translator_detail_url):
        response = owner_client.get(admin_translator_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_owner_can_patch_translator(self, owner_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson", about="Robert is very good! person")

        payload = {"name": "Updated name"}

        response = owner_client.patch(admin_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert translator.name == "Updated name"

    def test_admin_can_patch_translator(self, admin_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson", about="Robert is very good! person")

        payload = {"name": "Updated name"}

        response = admin_client.patch(admin_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert translator.name == "Updated name"

    def test_customer_cannot_patch_translator(self, customer_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson", about="Robert is very good! person")

        payload = {"name": "Updated name"}

        response = customer_client.patch(admin_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert translator.name == "Robert Johnson"

    def test_owner_can_put_translator(self, owner_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Old Translator", about="Old About")

        payload = {"name": "Updated Translator", "about": "Updated About"}

        response = owner_client.put(admin_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert translator.name == "Updated Translator"
        assert translator.about == "Updated About"

    def test_admin_can_put_translator(self, admin_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Old translator", about="Old About")

        payload = {"name": "Updated Translator", "about": "Updated About"}

        response = admin_client.put(admin_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert translator.name == "Updated Translator"
        assert translator.about == "Updated About"

    def test_customer_cannot_put_translator(self, customer_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Old Translator", about="Old About")

        payload = {"name": "Updated Translator", "about": "Updated About"}

        response = customer_client.put(admin_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert translator.name == "Old Translator"
        assert translator.about == "Old About"

    def test_owner_can_delete_translator(self, owner_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson")

        response = owner_client.delete(admin_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Translator.objects.filter(id=translator.id).exists()

    def test_admin_cannot_delete_translator(self, admin_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson")

        response = admin_client.delete(admin_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Translator.objects.filter(id=translator.id).exists()

    def test_customer_cannot_delete_translator(self, customer_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson")

        response = customer_client.delete(admin_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Translator.objects.filter(id=translator.id).exists()

    def test_translator_name_is_required_on_put(self, owner_client, translator_factory, admin_translator_detail_url):
        translator = translator_factory(name="Robert Johnson", about="Robert is very good! person")

        payload = {"about": "Updated About"}

        response = owner_client.put(admin_translator_detail_url(translator.pk), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_translator_name_must_be_unique_on_put(self, owner_client, translator_factory, admin_translator_detail_url):
        translator_factory(name="Robert Johnson", about="Robert is very good! person")
        second_translator = translator_factory(name="Jack Anderson", about="Jack is very good! person")

        payload = {"name": "Robert Johnson", "about": "Robert is very good! person"}

        response = owner_client.put(admin_translator_detail_url(second_translator.pk), payload)

        second_translator.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert second_translator.name == "Jack Anderson"

    def test_translator_name_must_be_unique_on_patch(
        self, owner_client, translator_factory, admin_translator_detail_url
    ):
        translator_factory(name="Robert Johnson", about="Robert is very good! person")
        second_translator = translator_factory(name="Jack Anderson", about="Jack is very good! person")

        payload = {"name": "Robert Johnson"}

        response = owner_client.patch(admin_translator_detail_url(second_translator.pk), payload)

        second_translator.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert second_translator.name == "Jack Anderson"

    def test_translator_read_only_fields_are_ignored_on_put(
        self, owner_client, translator_factory, admin_translator_detail_url
    ):
        translator = translator_factory(name="Robert Johnson", about="Robert is very good! person")

        old_id = translator.id
        old_created_at = translator.created_at

        payload = {
            "id": 999999,
            "name": "Updated Translator",
            "about": "Updated About",
            "created_at": "2000-01-01T00:00:00Z",
            "modified_at": "2000-01-01T00:00:00Z",
        }

        response = owner_client.put(admin_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert translator.id == old_id
        assert translator.created_at == old_created_at
        assert translator.name == "Updated Translator"
        assert translator.about == "Updated About"
