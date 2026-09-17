from datetime import timedelta

import pytest
from apps.books.models import Translator
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestTranslatorListApi:

    def test_get_translator_list(self, api_client, public_translator_list_url):
        response = api_client.get(public_translator_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_translator_list_returns_translators(self, api_client, translator_factory, public_translator_list_url):
        translator_factory(name="Translator 1")
        translator_factory(name="Translator 2")

        response = api_client.get(public_translator_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_translator_list_expected_fields(self, api_client, public_translator_list_url, translator_factory):
        translator = translator_factory(name="Robert Johnson")

        response = api_client.get(public_translator_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == translator.id
        assert set(results[0].keys()) == {"id", "name", "avatar"}
        assert results[0]["name"] == "Robert Johnson"

    def test_get_translator_list_ordered_by_created_at_desc(
        self, api_client, translator_factory, public_translator_list_url
    ):
        now = timezone.now()

        old = translator_factory(name="Old Translator")
        Translator.objects.filter(id=old.id).update(created_at=now - timedelta(days=2))

        new = translator_factory(name="New Translator")
        Translator.objects.filter(id=new.id).update(created_at=now)

        response = api_client.get(public_translator_list_url)

        results = response.data["results"]

        ids = [a["id"] for a in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [new.id, old.id]

    def test_get_translator_list_search_by_name(self, api_client, translator_factory, public_translator_list_url):
        target = translator_factory(name="Robert Johnson")

        translator_factory(name="Jack Anderson")

        response = api_client.get(public_translator_list_url, {"search": "Robe"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "Robert Johnson"

    def test_get_translator_list_search_is_case_insensitive(
        self, api_client, translator_factory, public_translator_list_url
    ):
        target = translator_factory(name="Robert Johnson")

        translator_factory(name="Jack Anderson")

        response = api_client.get(public_translator_list_url, {"search": "RoBe"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "Robert Johnson"

    def test_get_translator_list_search_returns_empty_list_when_no_match(
        self, api_client, translator_factory, public_translator_list_url
    ):
        translator_factory(name="Robert Johnson")
        translator_factory(name="Jack Anderson")

        response = api_client.get(public_translator_list_url, {"search": "Tesla"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results == []

    def test_get_translator_list_pagination_structure(self, api_client, translator_factory, public_translator_list_url):
        translator_factory(name="Translator 1")
        translator_factory(name="Translator 2")

        response = api_client.get(public_translator_list_url)

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

    def test_get_translator_list_default_page_size(self, api_client, translator_factory, public_translator_list_url):
        for i in range(30):
            translator_factory(name=f"Translator {i}")

        response = api_client.get(public_translator_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_translator_list_custom_page_size(self, api_client, translator_factory, public_translator_list_url):
        for i in range(20):
            translator_factory(name=f"Translator {i}")

        response = api_client.get(f"{public_translator_list_url}?page_size=10")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 20
        assert response.data["pages"] == 2

    def test_get_translator_list_page_size_respects_max_limit(
        self, api_client, translator_factory, public_translator_list_url
    ):
        for i in range(60):
            translator_factory(name=f"Translator {i}")

        response = api_client.get(f"{public_translator_list_url}?page_size=100")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_translator_list_next_link_exists_on_first_page(
        self, api_client, translator_factory, public_translator_list_url
    ):
        for i in range(30):
            translator_factory(name=f"Translator {i}")

        response = api_client.get(f"{public_translator_list_url}?page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_translator_list_previous_link_exists_on_second_page(
        self, api_client, translator_factory, public_translator_list_url
    ):
        for i in range(30):
            translator_factory(name=f"Translator {i}")

        response = api_client.get(f"{public_translator_list_url}?page=2&page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    def test_translator_list_post_not_allowed(self, api_client, public_translator_list_url):

        payload = {"name": "Robert Johnson"}

        response = api_client.post(public_translator_list_url, payload)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert not Translator.objects.filter(name="Robert Johnson").exists()


@pytest.mark.django_db
class TestTranslatorDetailApi:

    def test_get_translator_detail(self, api_client, translator_factory, public_translator_detail_url):
        translator = translator_factory(name="Robert Johnson", about="About Robert Johnson")

        response = api_client.get(public_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_get_translator_detail_returns_translator(
        self, api_client, translator_factory, public_translator_detail_url
    ):
        translator = translator_factory(name="Robert Johnson")
        response = api_client.get(public_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == translator.id
        assert response.data["name"] == translator.name

    def test_get_translator_detail_expected_fields(self, api_client, translator_factory, public_translator_detail_url):
        translator = translator_factory(name="Robert Johnson", about="About Robert Johnson")
        response = api_client.get(public_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {"id", "name", "avatar", "about"}
        assert response.data["name"] == "Robert Johnson"

    def test_get_translator_detail_not_found(self, api_client, public_translator_detail_url):
        response = api_client.get(public_translator_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_translator_detail_put_not_allowed(self, api_client, translator_factory, public_translator_detail_url):
        translator = translator_factory(name="Translator 1")

        payload = {"name": "Updated Translator"}

        response = api_client.put(public_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert translator.name == "Translator 1"

    def test_translator_detail_patch_not_allowed(self, api_client, translator_factory, public_translator_detail_url):
        translator = translator_factory(name="Translator 1")

        payload = {"name": "Updated Translator"}

        response = api_client.patch(public_translator_detail_url(translator.pk), payload)

        translator.refresh_from_db()

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert translator.name == "Translator 1"

    def test_translator_detail_delete_not_allowed(self, api_client, translator_factory, public_translator_detail_url):
        translator = translator_factory(name="Translator 1")
        response = api_client.delete(public_translator_detail_url(translator.pk))

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert Translator.objects.filter(id=translator.id).exists()
