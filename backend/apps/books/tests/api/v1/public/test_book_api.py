from datetime import timedelta

import pytest
from apps.books.models import Book
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestBookListApi:

    def test_get_book_list_returns_200(self, api_client, public_book_list_url):
        response = api_client.get(public_book_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_book_list_returns_only_active_books(self, api_client, book_factory, public_book_list_url):
        book_factory(is_active=True)
        book_factory(is_active=True)
        book_factory(is_active=False)

        response = api_client.get(public_book_list_url)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2

    def test_get_book_list_expected_fields(self, api_client, book_factory, public_book_list_url):
        book = book_factory(name="Clean Code", is_active=True)

        response = api_client.get(public_book_list_url)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book.id
        assert set(results[0].keys()) == {"id", "name", "avatar", "price", "language", "rating_average"}
        assert results[0]["name"] == "Clean Code"

    def test_get_book_list_language_field_returns_language_name(
        self, api_client, book_factory, language_factory, public_book_list_url
    ):
        language = language_factory(name="Persian")
        book_factory(language=language, is_active=True)

        response = api_client.get(public_book_list_url)
        results = response.data["results"]

        assert results[0]["language"] == "Persian"

    def test_get_book_list_rating_average_calculated_correctly(
        self, api_client, book_factory, rating_factory, public_book_list_url
    ):
        book = book_factory(is_active=True)
        # Ratings: 4 and 5 -> Avg = 4.5
        rating_factory(book=book, score=4)
        rating_factory(book=book, score=5)

        response = api_client.get(public_book_list_url)
        results = response.data["results"]

        assert results[0]["rating_average"] == 4.5

    def test_get_book_list_rating_average_defaults_to_zero_when_no_ratings(
        self, api_client, book_factory, public_book_list_url
    ):
        book_factory(is_active=True)

        response = api_client.get(public_book_list_url)
        results = response.data["results"]

        assert results[0]["rating_average"] == 0.0

    def test_get_book_list_ordered_by_created_at_desc_by_default(self, api_client, book_factory, public_book_list_url):
        now = timezone.now()
        book1 = book_factory(name="Older Book", is_active=True)
        book2 = book_factory(name="Newer Book", is_active=True)

        Book.objects.filter(id=book1.id).update(created_at=now - timedelta(days=2))
        Book.objects.filter(id=book2.id).update(created_at=now - timedelta(days=1))

        response = api_client.get(public_book_list_url)
        results = response.data["results"]

        assert results[0]["id"] == book2.id
        assert results[1]["id"] == book1.id

    # --------------------------------------------------------------------------
    # Search Filter Tests
    # --------------------------------------------------------------------------
    def test_get_book_list_search_by_book_name(self, api_client, book_factory, public_book_list_url):
        target_book = book_factory(name="Clean Code", is_active=True)
        book_factory(name="The Pragmatic Programmer", is_active=True)

        response = api_client.get(public_book_list_url, {"search": "Clean"})
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == target_book.id
        assert results[0]["name"] == "Clean Code"

    def test_get_book_list_search_by_author_name(self, api_client, book_factory, author_factory, public_book_list_url):
        author = author_factory(name="Robert C. Martin")
        book1 = book_factory(name="Book A", authors=[author], is_active=True)
        book_factory(name="Book B", is_active=True)

        response = api_client.get(public_book_list_url, {"search": "Martin"})
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == book1.id
        assert results[0]["name"] == "Book A"

    def test_get_book_list_search_is_case_insensitive(self, api_client, book_factory, public_book_list_url):
        book = book_factory(name="Refactoring", is_active=True)

        response = api_client.get(public_book_list_url, {"search": "rEfaCToR"})
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == book.id
        assert results[0]["name"] == "Refactoring"

    def test_get_book_list_search_returns_distinct_results_for_multiple_matching_authors(
        self, api_client, book_factory, author_factory, public_book_list_url
    ):
        # Even if multiple authors match the search string, the book shouldn't be duplicated
        author1 = author_factory(name="John Doe")
        author2 = author_factory(name="Johnny Smith")
        book = book_factory(name="Collaborative Work", authors=[author1, author2], is_active=True)

        response = api_client.get(public_book_list_url, {"search": "John"})
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["id"] == book.id

    def test_get_book_list_search_returns_empty_when_no_match(self, api_client, book_factory, public_book_list_url):
        book_factory(name="Clean Code", is_active=True)

        response = api_client.get(public_book_list_url, {"search": "NonExistent"})
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 0

    # --------------------------------------------------------------------------
    # Ordering Filter Tests
    # --------------------------------------------------------------------------
    def test_get_book_list_ordered_by_price_ascending(self, api_client, book_factory, public_book_list_url):
        book1 = book_factory(price=100_000, is_active=True)
        book2 = book_factory(price=50_000, is_active=True)

        response = api_client.get(public_book_list_url, {"ordering": "price"})
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book2.id
        assert results[1]["id"] == book1.id

    def test_get_book_list_ordered_by_price_descending(self, api_client, book_factory, public_book_list_url):
        book1 = book_factory(price=100_000, is_active=True)
        book2 = book_factory(price=50_000, is_active=True)

        response = api_client.get(public_book_list_url, {"ordering": "-price"})
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book1.id
        assert results[1]["id"] == book2.id

    # --------------------------------------------------------------------------
    # Pagination Tests
    # --------------------------------------------------------------------------
    def test_get_book_list_pagination_structure(self, api_client, book_factory, public_book_list_url):
        for i in range(30):
            book_factory(name=f"Book {i}", is_active=True)

        response = api_client.get(public_book_list_url)

        expected_keys = {
            "count",
            "pages",
            "current_page",
            "page_size",
            "next",
            "previous",
            "results",
        }
        assert set(response.data.keys()) == expected_keys
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1
        assert response.data["page_size"] == 20
        assert response.data["next"] is not None
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 20

    def test_get_book_list_default_page_size(self, api_client, book_factory, public_book_list_url):
        for i in range(30):
            book_factory(name=f"Book {i}", is_active=True)

        response = api_client.get(public_book_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 30
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_book_list_custom_page_size(self, api_client, book_factory, public_book_list_url):
        for i in range(15):
            book_factory(name=f"Book {i}", is_active=True)

        response = api_client.get(public_book_list_url, {"page_size": 10})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["pages"] == 2
        assert response.data["count"] == 15
        assert response.data["pages"] == 2

    def test_get_book_list_page_size_respects_max_limit(self, api_client, book_factory, public_book_list_url):
        for i in range(60):
            book_factory(name=f"Book {i}", is_active=True)

        response = api_client.get(public_book_list_url, {"page_size": 100})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_book_list_next_link_exists_on_first_page(self, api_client, book_factory, public_book_list_url):
        for i in range(30):
            book_factory(name=f"Book {i}", is_active=True)

        response = api_client.get(public_book_list_url, {"page_size": 10})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_book_list_previous_link_exists_on_second_page(self, api_client, book_factory, public_book_list_url):
        for i in range(30):
            book_factory(name=f"Book {i}", is_active=True)

        response = api_client.get(public_book_list_url, {"page": 2, "page_size": 10})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    # --------------------------------------------------------------------------
    # HTTP Method Not Allowed Tests
    # --------------------------------------------------------------------------
    def test_book_list_post_not_allowed(self, api_client, public_book_list_url):
        response = api_client.post(public_book_list_url, data={})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestBookDetailApi:

    def test_get_book_detail_returns_200(self, api_client, book_factory, public_book_detail_url):
        book = book_factory(is_active=True)

        response = api_client.get(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_200_OK

    def test_get_book_detail_inactive_book_returns_404(self, api_client, book_factory, public_book_detail_url):
        book = book_factory(is_active=False)

        response = api_client.get(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_book_detail_non_existent_id_returns_404(self, api_client, public_book_detail_url):

        response = api_client.get(public_book_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_book_detail_expected_fields(self, api_client, book_factory, public_book_detail_url):
        book = book_factory(name="Clean Code", is_active=True)

        response = api_client.get(public_book_detail_url(book.id))

        expected_fields = {
            "id",
            "name",
            "avatar",
            "price",
            "number_of_pages",
            "publication_date",
            "language",
            "inventory",
            "is_favorited",
            "rating_average",
            "ratings_count",
            "details",
            "authors",
            "translators",
            "categories",
            "publisher",
        }

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == expected_fields
        assert response.data["name"] == "Clean Code"

    def test_get_book_detail_nested_relationships_serialization(
        self,
        api_client,
        book_factory,
        author_factory,
        translator_factory,
        category_factory,
        publisher_factory,
        language_factory,
        book_detail_factory,
        public_book_detail_url,
    ):
        author = author_factory(name="Martin Fowler")
        translator = translator_factory(name="John Doe")
        category = category_factory(title="Software Engineering")
        publisher = publisher_factory(name="O'Reilly")
        language = language_factory(name="English")

        book = book_factory(
            name="Patterns of Enterprise Application Architecture",
            publisher=publisher,
            language=language,
            authors=[author],
            translators=[translator],
            category=[category],
            is_active=True,
        )

        detail_text = book_detail_factory(book=book, order=1, section_type="text", text="Introduction text")

        response = api_client.get(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["language"] == "English"
        assert response.data["publisher"] == {"id": publisher.id, "name": "O'Reilly"}
        assert response.data["authors"] == [{"id": author.id, "name": "Martin Fowler"}]
        assert response.data["translators"] == [{"id": translator.id, "name": "John Doe"}]
        assert response.data["categories"] == [{"id": category.id, "title": "Software Engineering"}]
        assert len(response.data["details"]) == 1
        assert response.data["details"][0]["id"] == detail_text.id
        assert response.data["details"][0]["order"] == 1
        assert response.data["details"][0]["text"] == "Introduction text"

    def test_get_book_detail_details_ordered_by_order_field(
        self, api_client, book_factory, book_detail_factory, public_book_detail_url
    ):
        book = book_factory(is_active=True)
        detail2 = book_detail_factory(book=book, order=2, text="Second section")
        detail1 = book_detail_factory(book=book, order=1, text="First section")

        response = api_client.get(public_book_detail_url(book.id))

        details = response.data["details"]

        assert response.status_code == status.HTTP_200_OK
        assert len(details) == 2
        assert details[0]["id"] == detail1.id
        assert details[1]["id"] == detail2.id

    def test_get_book_detail_ratings_count_and_average(
        self, api_client, book_factory, rating_factory, public_book_detail_url
    ):
        book = book_factory(is_active=True)
        rating_factory(book=book, score=4)
        rating_factory(book=book, score=5)
        rating_factory(book=book, score=3)

        response = api_client.get(public_book_detail_url(book.id))

        # (4 + 5 + 3) / 3 = 4.0
        assert response.status_code == status.HTTP_200_OK
        assert response.data["ratings_count"] == 3
        assert response.data["rating_average"] == 4.0

    def test_get_book_detail_ratings_default_values_when_no_ratings(
        self, api_client, book_factory, public_book_detail_url
    ):
        book = book_factory(is_active=True)

        response = api_client.get(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["ratings_count"] == 0
        assert response.data["rating_average"] == 0.0

    # --------------------------------------------------------------------------
    # Authentication & is_favorited Tests
    # --------------------------------------------------------------------------
    def test_get_book_detail_is_favorited_always_false_for_anonymous_user(
        self, api_client, book_factory, public_book_detail_url
    ):
        book = book_factory(is_active=True)

        response = api_client.get(public_book_detail_url(book.id))

        assert response.data["is_favorited"] is False

    def test_get_book_detail_is_favorited_true_when_authenticated_user_favorited_book(
        self,
        customer_client,
        customer_user,
        book_factory,
        favorite_factory,
        public_book_detail_url,
    ):
        book = book_factory(is_active=True)
        favorite_factory(user=customer_user, book=book)

        response = customer_client.get(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_favorited"] is True

    def test_get_book_detail_is_favorited_false_when_authenticated_user_has_not_favorited_book(
        self,
        customer_client,
        book_factory,
        public_book_detail_url,
    ):
        book = book_factory(is_active=True)

        response = customer_client.get(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_favorited"] is False

    def test_get_book_detail_is_favorited_false_when_another_user_favorited_book(
        self,
        customer_client,
        user_factory,
        book_factory,
        favorite_factory,
        public_book_detail_url,
    ):
        other_user = user_factory()
        book = book_factory(is_active=True)
        favorite_factory(user=other_user, book=book)

        response = customer_client.get(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_favorited"] is False

    # --------------------------------------------------------------------------
    # HTTP Method Not Allowed Tests
    # --------------------------------------------------------------------------
    def test_book_detail_put_not_allowed(self, api_client, book_factory, public_book_detail_url):
        book = book_factory(is_active=True)

        response = api_client.put(public_book_detail_url(book.id), data={})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_book_detail_patch_not_allowed(self, api_client, book_factory, public_book_detail_url):
        book = book_factory(is_active=True)

        response = api_client.patch(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_book_detail_delete_not_allowed(self, api_client, book_factory, public_book_detail_url):
        book = book_factory(is_active=True)

        response = api_client.delete(public_book_detail_url(book.id))

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
