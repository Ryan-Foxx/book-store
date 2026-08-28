from datetime import date, timedelta

import pytest
from apps.books.models import Award
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestAwardListApi:

    def test_owner_can_get_award_list(self, owner_client, admin_award_list_url):
        response = owner_client.get(admin_award_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_award_list(self, admin_client, admin_award_list_url):
        response = admin_client.get(admin_award_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_award_list(self, customer_client, admin_award_list_url):
        response = customer_client.get(admin_award_list_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_award_list(self, api_client, admin_award_list_url):
        response = api_client.get(admin_award_list_url)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_owner_get_award_list_returns_awards(self, owner_client, award_factory, admin_award_list_url):
        award_factory(title="Award 1")
        award_factory(title="Award 2")

        response = owner_client.get(admin_award_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_admin_get_award_list_returns_awards(self, admin_client, award_factory, admin_award_list_url):
        award_factory(title="Award 1")
        award_factory(title="Award 2")

        response = admin_client.get(admin_award_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_award_list_expected_fields(self, owner_client, award_factory, author_factory, admin_award_list_url):
        author = author_factory(name="Author 1")
        award = award_factory(title="Nobel Prize", year_received=date(2020, 5, 10))
        award.authors.add(author)

        response = owner_client.get(admin_award_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == award.id
        assert set(results[0].keys()) == {"id", "authors", "title", "year_received", "created_at", "modified_at"}
        assert results[0]["authors"] == [{"id": author.id, "name": author.name}]
        assert results[0]["title"] == "Nobel Prize"
        assert results[0]["year_received"] == "2020-05-10"

    def test_get_award_list_ordered_by_modified_at_desc(self, owner_client, award_factory, admin_award_list_url):
        now = timezone.now()

        old = award_factory(title="Old Award")
        Award.objects.filter(id=old.id).update(modified_at=now - timedelta(days=2))

        new = award_factory(title="New Award")
        Award.objects.filter(id=new.id).update(modified_at=now)

        response = owner_client.get(admin_award_list_url)

        results = response.data["results"]
        ids = [award["id"] for award in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [new.id, old.id]

    def test_get_award_list_search_by_title(self, owner_client, award_factory, admin_award_list_url):
        target = award_factory(title="(NSA)")
        award_factory(title="Award 1")

        response = owner_client.get(admin_award_list_url, {"search": "nSa"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["title"] == "(NSA)"

    def test_get_award_list_search_by_author_name(
        self, owner_client, author_factory, award_factory, admin_award_list_url
    ):
        target_author = author_factory(name="J. K. Rowling")
        another_author = author_factory(name="George Orwell")

        target_award = award_factory(title="Literary Award")
        another_award = award_factory(title="Book Award")

        target_award.authors.add(target_author)
        another_award.authors.add(another_author)

        response = owner_client.get(admin_award_list_url, {"search": "rowling"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target_award.id

    def test_get_award_list_search_is_case_insensitive(self, owner_client, award_factory, admin_award_list_url):
        target = award_factory(title="Nobel Prize")
        award_factory(title="(NSA)")

        response = owner_client.get(admin_award_list_url, {"search": "NoBeL"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target.id
        assert results[0]["title"] == "Nobel Prize"

    def test_get_award_list_search_returns_empty_list_when_no_match(
        self, owner_client, award_factory, admin_award_list_url
    ):
        award_factory(title="Nobel Prize")
        award_factory(title="Pulitzer Prize")

        response = owner_client.get(admin_award_list_url, {"search": "Oscar"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results == []

    def test_get_award_list_ordering_by_id(self, owner_client, award_factory, admin_award_list_url):
        first = award_factory(title="Award 1")
        second = award_factory(title="Award 2")
        third = award_factory(title="Award 3")

        response = owner_client.get(admin_award_list_url, {"ordering": "id"})

        results = response.data["results"]
        ids = [award["id"] for award in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [first.id, second.id, third.id]

    def test_get_award_list_ordering_by_id_desc(self, owner_client, award_factory, admin_award_list_url):
        first = award_factory(title="Award 1")
        second = award_factory(title="Award 2")
        third = award_factory(title="Award 3")

        response = owner_client.get(admin_award_list_url, {"ordering": "-id"})

        results = response.data["results"]
        ids = [award["id"] for award in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [third.id, second.id, first.id]

    def test_get_award_list_ordering_by_year_received(self, owner_client, award_factory, admin_award_list_url):
        first = award_factory(title="Award 1", year_received=date(2010, 1, 1))
        second = award_factory(title="Award 2", year_received=date(2020, 1, 1))

        response = owner_client.get(admin_award_list_url, {"ordering": "year_received"})

        results = response.data["results"]
        ids = [award["id"] for award in results]

        assert response.status_code == status.HTTP_200_OK
        assert ids == [first.id, second.id]

    def test_get_award_list_ordering_by_created_at(self, owner_client, award_factory, admin_award_list_url):
        first = award_factory(title="Award 1")
        second = award_factory(title="Award 2")

        response = owner_client.get(admin_award_list_url, {"ordering": "created_at"})

        results = response.data["results"]
        ids = [award["id"] for award in results]

        assert response.status_code == status.HTTP_200_OK
        assert set(ids) == {first.id, second.id}

    def test_get_award_list_ordering_by_modified_at(self, owner_client, award_factory, admin_award_list_url):
        first = award_factory(title="Award 1")
        second = award_factory(title="Award 2")

        response = owner_client.get(admin_award_list_url, {"ordering": "-modified_at"})

        results = response.data["results"]
        ids = [award["id"] for award in results]

        assert response.status_code == status.HTTP_200_OK
        assert set(ids) == {first.id, second.id}

    def test_get_award_list_pagination_structure(self, owner_client, award_factory, admin_award_list_url):
        award_factory(title="award 1")
        award_factory(title="award 2")

        response = owner_client.get(admin_award_list_url)

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

    def test_get_award_list_default_page_size(self, owner_client, award_factory, admin_award_list_url):
        for i in range(30):
            award_factory(title=f"Award {i}")

        response = owner_client.get(admin_award_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_award_list_custom_page_size(self, owner_client, award_factory, admin_award_list_url):
        for i in range(20):
            award_factory(title=f"Award {i}")

        response = owner_client.get(f"{admin_award_list_url}?page_size=10")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 20
        assert response.data["pages"] == 2

    def test_get_award_list_page_size_respects_max_limit(self, owner_client, award_factory, admin_award_list_url):
        for i in range(60):
            award_factory(title=f"Award {i}")

        response = owner_client.get(f"{admin_award_list_url}?page_size=100")

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_award_list_next_link_exists_on_first_page(self, owner_client, award_factory, admin_award_list_url):
        for i in range(30):
            award_factory(title=f"Award {i}")

        response = owner_client.get(f"{admin_award_list_url}?page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_award_list_previous_link_exists_on_second_page(
        self, owner_client, award_factory, admin_award_list_url
    ):
        for i in range(30):
            award_factory(title=f"Award {i}")

        response = owner_client.get(f"{admin_award_list_url}?page=2&page_size=10")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    def test_owner_can_create_award(self, owner_client, author_factory, admin_award_list_url):
        author = author_factory(name="Author 1")

        payload = {"title": "Nobel Prize", "year_received": "2020-05-10", "authors": [author.id]}

        response = owner_client.post(admin_award_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Award.objects.filter(title="Nobel Prize").exists()

    def test_admin_can_create_award(self, admin_client, author_factory, admin_award_list_url):
        author = author_factory(name="Author 1")

        payload = {"title": "Nobel Prize", "year_received": "2020-05-10", "authors": [author.id]}

        response = admin_client.post(admin_award_list_url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Award.objects.filter(title="Nobel Prize").exists()

    def test_customer_cannot_create_award(self, customer_client, author_factory, admin_award_list_url):
        author = author_factory(name="Author 1")

        payload = {"title": "Nobel Prize", "year_received": "2020-05-10", "authors": [author.id]}

        response = customer_client.post(admin_award_list_url, payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Award.objects.filter(title="Nobel Prize").exists()

    def test_award_title_is_required(self, owner_client, admin_award_list_url):
        payload = {"year_received": "2020-05-10"}

        response = owner_client.post(admin_award_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_award_title_must_be_unique(self, owner_client, award_factory, admin_award_list_url):
        award_factory(title="Nobel Prize")

        payload = {"title": "Nobel Prize", "year_received": "2020-05-10"}

        response = owner_client.post(admin_award_list_url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_award_can_be_created_without_authors(self, owner_client, admin_award_list_url):
        payload = {"title": "Nobel Prize", "year_received": "2020-05-10"}

        response = owner_client.post(admin_award_list_url, payload)

        award = Award.objects.get(title="Nobel Prize")

        assert response.status_code == status.HTTP_201_CREATED
        assert award.authors.count() == 0

    def test_award_authors_must_be_valid(self, owner_client, admin_award_list_url):
        response = owner_client.post(admin_award_list_url, {"title": "Invalid Author Award", "authors": [999999]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "authors" in response.data


@pytest.mark.django_db
class TestAwardDetailApi:

    def test_owner_can_get_award_detail(self, owner_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received="2020-05-10")

        response = owner_client.get(admin_award_detail_url(award.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_award_detail(self, admin_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received="2020-05-10")

        response = admin_client.get(admin_award_detail_url(award.pk))

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_award_detail(self, customer_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received="2020-05-10")

        response = customer_client.get(admin_award_detail_url(award.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_award_detail(self, api_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received="2020-05-10")

        response = api_client.get(admin_award_detail_url(award.pk))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_award_detail_returns_award(self, owner_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received="2020-05-10")

        response = owner_client.get(admin_award_detail_url(award.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == award.id
        assert response.data["title"] == award.title

    def test_get_award_detail_fields(self, owner_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received=date(2020, 5, 10))

        response = owner_client.get(admin_award_detail_url(award.pk))

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {"id", "authors", "title", "year_received", "created_at", "modified_at"}
        assert response.data["authors"] == []
        assert response.data["title"] == "Nobel Prize"
        assert response.data["year_received"] == "2020-05-10"

    def test_get_award_detail_returns_authors(
        self, owner_client, author_factory, award_factory, admin_award_detail_url
    ):
        author_1 = author_factory(name="Author 1")
        author_2 = author_factory(name="Author 2")

        award = award_factory(title="Shared Award", year_received=date(2020, 5, 10))
        award.authors.add(author_1, author_2)

        response = owner_client.get(admin_award_detail_url(award.pk))

        author_ids = [author["id"] for author in response.data["authors"]]

        assert response.status_code == status.HTTP_200_OK
        assert set(author_ids) == {author_1.id, author_2.id}

    def test_get_award_detail_not_found(self, owner_client, admin_award_detail_url):
        response = owner_client.get(admin_award_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_owner_can_patch_award(self, owner_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Shared Award", year_received=date(2020, 5, 10))

        response = owner_client.patch(admin_award_detail_url(award.pk), {"title": "Updated Title"})

        award.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert award.title == "Updated Title"
        assert award.year_received == date(2020, 5, 10)

    def test_admin_can_patch_award(self, admin_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Shared Award", year_received=date(2020, 5, 10))

        response = admin_client.patch(admin_award_detail_url(award.pk), {"title": "Updated Title"})

        award.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert award.title == "Updated Title"
        assert award.year_received == date(2020, 5, 10)

    def test_customer_cannot_patch_award(self, customer_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Shared Award", year_received=date(2020, 5, 10))

        response = customer_client.patch(admin_award_detail_url(award.pk), {"title": "Updated Title"})

        award.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert award.title == "Shared Award"

    def test_owner_can_put_award(self, owner_client, author_factory, award_factory, admin_award_detail_url):
        old_author = author_factory(name="Old Author")
        new_author = author_factory(name="New Author")

        award = award_factory(title="Old Award", year_received=date(2020, 1, 1))
        award.authors.add(old_author)

        payload = {"title": "Updated Award", "year_received": "2022-05-10", "authors": [new_author.id]}

        response = owner_client.put(admin_award_detail_url(award.pk), payload)

        award.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert award.title == "Updated Award"
        assert award.year_received == date(2022, 5, 10)
        assert list(award.authors.values_list("id", flat=True)) == [new_author.id]

    def test_admin_can_put_award(self, admin_client, author_factory, award_factory, admin_award_detail_url):
        old_author = author_factory(name="Old Author")
        new_author = author_factory(name="New Author")

        award = award_factory(title="Old Award", year_received=date(2020, 1, 1))
        award.authors.add(old_author)

        payload = {"title": "Updated Award", "year_received": "2022-05-10", "authors": [new_author.id]}

        response = admin_client.put(admin_award_detail_url(award.pk), payload)

        award.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert award.title == "Updated Award"
        assert award.year_received == date(2022, 5, 10)
        assert list(award.authors.values_list("id", flat=True)) == [new_author.id]

    def test_customer_cannot_put_award(self, customer_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Old Award", year_received=date(2020, 1, 1))

        payload = {"title": "Updated Award", "year_received": "2022-05-10"}

        response = customer_client.put(admin_award_detail_url(award.pk), payload)

        award.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert award.title == "Old Award"

    def test_owner_can_delete_award(self, owner_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received=date(2020, 1, 1))

        response = owner_client.delete(admin_award_detail_url(award.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Award.objects.filter(id=award.id).exists()

    def test_admin_cannot_delete_award(self, admin_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received=date(2020, 1, 1))

        response = admin_client.delete(admin_award_detail_url(award.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Award.objects.filter(id=award.id).exists()

    def test_customer_cannot_delete_award(self, customer_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received=date(2020, 1, 1))

        response = customer_client.delete(admin_award_detail_url(award.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Award.objects.filter(id=award.id).exists()

    def test_award_title_is_required_on_put(self, owner_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Nobel Prize", year_received=date(2020, 1, 1))

        payload = {"authors": [], "year_received": "2022-05-05"}

        response = owner_client.put(admin_award_detail_url(award.pk), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_award_title_must_be_unique_on_update(self, owner_client, award_factory, admin_award_detail_url):
        award_factory(title="First Award", year_received=date(2020, 1, 1))
        second_award = award_factory(title="Second Award", year_received=date(2022, 1, 1))

        payload = {"title": "First Award"}

        response = owner_client.patch(admin_award_detail_url(second_award.pk), payload)

        second_award.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
        assert second_award.title == "Second Award"

    def test_read_only_fields_are_ignored_on_put(self, owner_client, award_factory, admin_award_detail_url):
        award = award_factory(title="Old Award", year_received=date(2020, 1, 1))

        award.refresh_from_db()

        old_id = award.id
        old_created_at = award.created_at

        payload = {
            "id": 999999,
            "title": "Updated Award",
            "year_received": "2022-01-01",
            "authors": [],
            "created_at": "2000-01-01T00:00:00Z",
            "modified_at": "2000-01-01T00:00:00Z",
        }

        response = owner_client.put(admin_award_detail_url(award.pk), payload)

        award.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert award.id == old_id
        assert award.created_at == old_created_at
        assert award.title == "Updated Award"
        assert award.year_received == date(2022, 1, 1)
