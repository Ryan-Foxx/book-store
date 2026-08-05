from datetime import timedelta

import pytest
from apps.books.models import Author
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestAdminAuthorListApi:

    def test_owner_can_get_author_list(self, owner_client, admin_author_list_url):
        response = owner_client.get(admin_author_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_author_list(self, admin_client, admin_author_list_url):
        response = admin_client.get(admin_author_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_author_list(self, customer_client, admin_author_list_url):
        response = customer_client.get(admin_author_list_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_author_list(self, api_client, admin_author_list_url):
        response = api_client.get(admin_author_list_url)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_owner_get_author_list_returns_authors(self, owner_client, author_factory, admin_author_list_url):
        author_factory(name="Author 1")
        author_factory(name="Author 2")

        response = owner_client.get(admin_author_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_admin_get_author_list_returns_authors(self, admin_client, author_factory, admin_author_list_url):
        author_factory(name="Author 1")
        author_factory(name="Author 2")

        response = admin_client.get(admin_author_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_author_list_expected_fields(self, owner_client, author_factory, admin_author_list_url):
        author = author_factory(name="Author 1")

        response = owner_client.get(admin_author_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == author.id
        assert set(results[0].keys()) == {
            "id",
            "name",
            "avatar",
            "about",
            "biography",
            "created_at",
            "modified_at",
        }

    def test_get_author_list_ordered_by_modified_at_desc(self, owner_client, author_factory, admin_author_list_url):
        now = timezone.now()

        old = author_factory(name="Old Author")
        Author.objects.filter(id=old.id).update(modified_at=now - timedelta(days=2))

        new = author_factory(name="New Author")
        Author.objects.filter(id=new.id).update(modified_at=now)

        response = owner_client.get(admin_author_list_url)

        results = response.data["results"]
        ids = [author["id"] for author in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [new.id, old.id]

    def test_get_author_list_search_by_name(self, owner_client, author_factory, admin_author_list_url):
        target = author_factory(name="J. K. Rowling")
        author_factory(name="George Orwell")

        response = owner_client.get(admin_author_list_url, {"search": "row"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "J. K. Rowling"

    def test_get_author_list_search_is_case_insensitive(self, owner_client, author_factory, admin_author_list_url):
        target = author_factory(name="J. K. Rowling")
        author_factory(name="George Orwell")

        response = owner_client.get(admin_author_list_url, {"search": "ROW"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "J. K. Rowling"

    def test_get_author_list_search_returns_empty_list_when_no_match(
        self, owner_client, author_factory, admin_author_list_url
    ):
        author_factory(name="J. K. Rowling")
        author_factory(name="George Orwell")

        response = owner_client.get(admin_author_list_url, {"search": "tolkien"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results == []

    def test_get_author_list_ordering_by_id(self, owner_client, author_factory, admin_author_list_url):
        first = author_factory(name="Author 1")
        second = author_factory(name="Author 2")
        third = author_factory(name="Author 3")

        response = owner_client.get(admin_author_list_url, {"ordering": "id"})

        results = response.data["results"]
        ids = [author["id"] for author in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [first.id, second.id, third.id]

    def test_get_author_list_ordering_by_id_desc(self, owner_client, author_factory, admin_author_list_url):
        first = author_factory(name="Author 1")
        second = author_factory(name="Author 2")
        third = author_factory(name="Author 3")

        response = owner_client.get(admin_author_list_url, {"ordering": "-id"})

        results = response.data["results"]
        ids = [author["id"] for author in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [third.id, second.id, first.id]

    def test_get_author_list_pagination_structure(self, owner_client, author_factory, admin_author_list_url):
        author_factory(name="Author 1")
        author_factory(name="Author 2")

        response = owner_client.get(admin_author_list_url)

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

    def test_get_author_list_default_page_size(self, owner_client, author_factory, admin_author_list_url):
        for i in range(30):
            author_factory(name=f"Author {i}")

        response = owner_client.get(admin_author_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_author_list_custom_page_size(self, owner_client, author_factory, admin_author_list_url):
        for i in range(20):
            author_factory(name=f"Author {i}")

        response = owner_client.get(f"{admin_author_list_url}?page_size=10")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 20
        assert response.data["pages"] == 2

    def test_get_author_list_page_size_respects_max_limit(self, owner_client, author_factory, admin_author_list_url):
        for i in range(60):
            author_factory(name=f"Author {i}")

        response = owner_client.get(f"{admin_author_list_url}?page_size=100")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_author_list_next_link_exists_on_first_page(self, owner_client, author_factory, admin_author_list_url):
        for i in range(30):
            author_factory(name=f"Author {i}")

        response = owner_client.get(f"{admin_author_list_url}?page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_author_list_previous_link_exists_on_second_page(
        self, owner_client, author_factory, admin_author_list_url
    ):
        for i in range(30):
            author_factory(name=f"Author {i}")

        response = owner_client.get(f"{admin_author_list_url}?page=2&page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    def test_owner_can_create_author(self, owner_client, admin_author_list_url):
        payload = {
            "name": "Fyodor Dostoevsky",
            "about": "Russian novelist",
            "biography": "Author of Crime and Punishment",
        }

        response = owner_client.post(admin_author_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(name="Fyodor Dostoevsky").exists()

    def test_admin_cannot_create_author(self, admin_client, admin_author_list_url):
        payload = {
            "name": "Admin Created Author",
            "about": "About",
            "biography": "Biography",
        }

        response = admin_client.post(admin_author_list_url, payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Author.objects.filter(name="Admin Created Author").exists()

    def test_customer_cannot_create_author(self, customer_client, admin_author_list_url):
        payload = {
            "name": "Customer Created Author",
            "about": "About",
            "biography": "Biography",
        }

        response = customer_client.post(admin_author_list_url, payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Author.objects.filter(name="Customer Created Author").exists()

    def test_author_name_is_required(self, owner_client, admin_author_list_url):
        payload = {
            "about": "About without name",
            "biography": "Biography without name",
        }

        response = owner_client.post(admin_author_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_author_name_must_be_unique(self, owner_client, author_factory, admin_author_list_url):
        author_factory(name="Unique Author")

        payload = {
            "name": "Unique Author",
            "about": "Another about",
            "biography": "Another biography",
        }

        response = owner_client.post(admin_author_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data


@pytest.mark.django_db
class TestAdminAuthorDetailApi:

    def test_owner_can_get_author_detail(self, owner_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Alice")

        response = owner_client.get(admin_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_author_detail(self, admin_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Alice")

        response = admin_client.get(admin_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_author_detail(self, customer_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Alice")

        response = customer_client.get(admin_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_author_detail_returns_author(self, owner_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Alice")

        response = owner_client.get(admin_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == author.id
        assert response.data["name"] == author.name

    def test_get_author_detail_fields(self, owner_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Alice", about="About Alice", biography="Biography Alice")

        response = owner_client.get(admin_author_detail_url(author.pk))

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert set(data.keys()) == {
            "id",
            "name",
            "avatar",
            "about",
            "biography",
            "created_at",
            "modified_at",
        }

    def test_get_author_detail_not_found(self, owner_client, admin_author_detail_url):
        response = owner_client.get(admin_author_detail_url(999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_owner_can_patch_author(self, owner_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1", about="Old about")

        response = owner_client.patch(admin_author_detail_url(author.pk), {"about": "Updated about"})

        author.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert author.about == "Updated about"

    def test_admin_can_patch_author(self, admin_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1")

        response = admin_client.patch(admin_author_detail_url(author.pk), {"name": "Updated Author"})

        author.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert author.name == "Updated Author"

    def test_customer_cannot_patch_author(self, customer_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1")

        response = customer_client.patch(admin_author_detail_url(author.pk), {"name": "Updated Author"})

        author.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert author.name == "Author 1"

    def test_owner_can_put_author(self, owner_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1", about="Old about", biography="Old biography")

        payload = {
            "name": "Updated Author",
            "about": "Updated about",
            "biography": "Updated biography",
        }

        response = owner_client.put(admin_author_detail_url(author.pk), payload)

        author.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert author.name == "Updated Author"
        assert author.about == "Updated about"
        assert author.biography == "Updated biography"

    def test_admin_can_put_author(self, admin_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1", about="Old about", biography="Old biography")

        payload = {
            "name": "Updated Author",
            "about": "Updated about",
            "biography": "Updated biography",
        }

        response = admin_client.put(admin_author_detail_url(author.pk), payload)

        author.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert author.name == "Updated Author"
        assert author.about == "Updated about"
        assert author.biography == "Updated biography"

    def test_customer_cannot_put_author(self, customer_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1", about="Old about", biography="Old biography")

        payload = {
            "name": "Updated Author",
            "about": "Updated about",
            "biography": "Updated biography",
        }

        response = customer_client.put(admin_author_detail_url(author.pk), payload)

        author.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert author.name == "Author 1"

    def test_owner_can_delete_author(self, owner_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1")

        response = owner_client.delete(admin_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(id=author.id).exists()

    def test_admin_cannot_delete_author(self, admin_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1")

        response = admin_client.delete(admin_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Author.objects.filter(id=author.id).exists()

    def test_customer_cannot_delete_author(self, customer_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1")

        response = customer_client.delete(admin_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Author.objects.filter(id=author.id).exists()

    def test_read_only_fields_are_ignored_on_put(self, owner_client, author_factory, admin_author_detail_url):
        author = author_factory(name="Author 1", about="Old about", biography="Old biography")
        author.refresh_from_db()

        old_id = author.id
        old_created_at = author.created_at

        payload = {
            "id": 999,
            "name": "Updated Author",
            "about": "Updated about",
            "biography": "Updated biography",
            "created_at": "2000-01-01T00:00:00Z",
            "modified_at": "2000-01-01T00:00:00Z",
        }

        response = owner_client.put(admin_author_detail_url(author.pk), payload)

        author.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert author.id == old_id
        assert author.created_at == old_created_at
        assert author.name == "Updated Author"
