from datetime import date, timedelta

import pytest
from apps.books.models import Author
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestAuthorListApi:

    def test_get_author_list_status_200(self, api_client, public_author_list_url):
        response = api_client.get(public_author_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_author_list_returns_authors(self, api_client, author_factory, public_author_list_url):
        author_factory(name="Author 1")
        author_factory(name="Author 2")

        response = api_client.get(public_author_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_author_list_expected_fields(self, api_client, public_author_list_url, author_factory):
        author = author_factory(name="Author 1")

        response = api_client.get(public_author_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == author.id
        assert set(results[0].keys()) == {"id", "name", "avatar"}

    def test_get_author_list_ordered_by_created_at_desc(self, api_client, author_factory, public_author_list_url):
        now = timezone.now()

        old = author_factory(name="Old Author")
        Author.objects.filter(id=old.id).update(created_at=now - timedelta(days=2))

        new = author_factory(name="New Author")
        Author.objects.filter(id=new.id).update(created_at=now)

        response = api_client.get(public_author_list_url)

        results = response.data["results"]

        ids = [a["id"] for a in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [new.id, old.id]

    def test_get_author_list_search_by_name(self, api_client, author_factory, public_author_list_url):
        target = author_factory(name="J. K. Rowling")

        author_factory(name="George Orwell")

        response = api_client.get(public_author_list_url, {"search": "row"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "J. K. Rowling"

    def test_get_author_list_search_is_case_insensitive(self, api_client, author_factory, public_author_list_url):
        target = author_factory(name="J. K. Rowling")

        author_factory(name="George Orwell")

        response = api_client.get(public_author_list_url, {"search": "ROW"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["name"] == "J. K. Rowling"

    def test_get_author_list_search_returns_empty_list_when_no_match(self, api_client, author_factory, public_author_list_url):
        author_factory(name="J. K. Rowling")
        author_factory(name="George Orwell")

        response = api_client.get(public_author_list_url, {"search": "tolkien"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results == []

    def test_get_author_list_pagination_structure(self, api_client, author_factory, public_author_list_url):
        author_factory(name="Author 1")
        author_factory(name="Author 2")

        response = api_client.get(public_author_list_url)

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
        assert response.data["page_size"] == 10
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 2

    def test_get_author_list_default_page_size(self, api_client, author_factory, public_author_list_url):
        for i in range(15):
            author_factory(name=f"Author {i}")

        response = api_client.get(public_author_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 15
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_author_list_custom_page_size(self, api_client, author_factory, public_author_list_url):
        for i in range(10):
            author_factory(name=f"Author {i}")

        response = api_client.get(f"{public_author_list_url}?page_size=5")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 5
        assert response.data["page_size"] == 5
        assert response.data["count"] == 10
        assert response.data["pages"] == 2

    def test_get_author_list_page_size_respects_max_limit(self, api_client, author_factory, public_author_list_url):
        for i in range(60):
            author_factory(name=f"Author {i}")

        response = api_client.get(f"{public_author_list_url}?page_size=100")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_author_post_not_allowed(self, api_client, public_author_list_url):
        response = api_client.post(public_author_list_url, {"name": "New Author"})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestAuthorDetailApi:

    def test_get_author_detail_status_200(self, api_client, author_factory, public_author_detail_url):
        author = author_factory(name="Alice", about="About Alice", biography="Biography Alice")

        response = api_client.get(public_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_get_author_detail_returns_author(self, api_client, author_factory, public_author_detail_url):
        author = author_factory(name="Alice")
        response = api_client.get(public_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == author.id

    def test_get_author_detail_fields(self, api_client, author_factory, public_author_detail_url):
        author = author_factory(name="Alice", about="About Alice", biography="Biography Alice")
        response = api_client.get(public_author_detail_url(author.pk))

        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert set(data.keys()) == {"id", "name", "avatar", "about", "biography", "awards"}

    def test_get_author_detail_returns_empty_awards_when_author_has_no_awards(
        self, api_client, author_factory, public_author_detail_url
    ):
        author = author_factory(name="Alice")

        response = api_client.get(public_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["awards"] == []

    def test_get_author_detail_returns_author_awards(
        self, api_client, author_factory, award_factory, public_author_detail_url
    ):
        author = author_factory(name="J. K. Rowling")

        award = award_factory(title="British Book Award", year_received=date(1998, 5, 10))
        award.authors.add(author)

        response = api_client.get(public_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_200_OK

        assert response.data["awards"] == [
            {"id": award.id, "title": "British Book Award", "year_received": "1998-05-10"}
        ]

    def test_get_author_detail_returns_multiple_awards(
        self, api_client, author_factory, award_factory, public_author_detail_url
    ):
        author = author_factory(name="J. K. Rowling")

        award_1 = award_factory(title="Award One", year_received=date(1997, 1, 1))
        award_2 = award_factory(title="Award Two", year_received=date(2000, 2, 2))

        award_1.authors.add(author)
        award_2.authors.add(author)

        response = api_client.get(public_author_detail_url(author.pk))

        awards = response.data["awards"]

        assert response.status_code == status.HTTP_200_OK
        assert len(awards) == 2

        assert {(award["id"], award["title"], award["year_received"]) for award in awards} == {
            (award_1.id, "Award One", "1997-01-01"),
            (award_2.id, "Award Two", "2000-02-02"),
        }

    def test_get_author_detail_does_not_return_other_authors_awards(
        self, api_client, author_factory, award_factory, public_author_detail_url
    ):
        target_author = author_factory(name="J. K. Rowling")
        another_author = author_factory(name="George Orwell")

        target_award = award_factory(title="Target Author Award")
        other_award = award_factory(title="Other Author Award")

        target_award.authors.add(target_author)
        other_award.authors.add(another_author)

        response = api_client.get(public_author_detail_url(target_author.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["awards"] == [
            {"id": target_award.id, "title": "Target Author Award", "year_received": None}
        ]

    def test_get_author_detail_not_found(self, api_client, public_author_detail_url):
        response = api_client.get(public_author_detail_url(999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_author_detail_put_not_allowed(self, api_client, author_factory, public_author_detail_url):
        author = author_factory(name="Author 1")
        response = api_client.put(public_author_detail_url(author.pk), {"name": "Updated Author"})

        author.refresh_from_db()

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert author.name == "Author 1"

    def test_author_detail_patch_not_allowed(self, api_client, author_factory, public_author_detail_url):
        author = author_factory(name="Author 1")
        response = api_client.patch(public_author_detail_url(author.pk), {"name": "Updated Author"})

        author.refresh_from_db()

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert author.name == "Author 1"

    def test_author_detail_delete_not_allowed(self, api_client, author_factory, public_author_detail_url):
        author = author_factory(name="Author 1")
        response = api_client.delete(public_author_detail_url(author.pk))

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert Author.objects.filter(id=author.id).exists()
