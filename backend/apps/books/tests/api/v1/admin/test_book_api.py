import pytest
from apps.books.models import Book
from rest_framework import status

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def book_payload(author_factory, translator_factory, category_factory, publisher_factory, language_factory):
    author = author_factory()
    translator = translator_factory()
    category = category_factory()
    publisher = publisher_factory()
    language = language_factory()

    return {
        "name": "Clean Code",
        "price": 150000,
        "number_of_pages": 464,
        "publication_date": "2008-08-01",
        "inventory": 10,
        "is_active": True,
        "authors": [author.id],
        "translators": [translator.id],
        "category": [category.id],
        "publisher": publisher.id,
        "language": language.id,
    }


@pytest.mark.django_db
class TestBookListApi:

    # --------------------------------------------------------------------------
    # Permissions
    # --------------------------------------------------------------------------
    def test_owner_can_get_book_list(self, owner_client, admin_book_list_url):
        response = owner_client.get(admin_book_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_book_list(self, admin_client, admin_book_list_url):
        response = admin_client.get(admin_book_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_book_list(self, customer_client, admin_book_list_url):
        response = customer_client.get(admin_book_list_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_book_list(self, api_client, admin_book_list_url):
        response = api_client.get(admin_book_list_url)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    # --------------------------------------------------------------------------
    # Response Structure & Inactive Books Visibility
    # --------------------------------------------------------------------------
    def test_get_book_list_expected_fields(self, admin_client, book_factory, admin_book_list_url):
        book_factory(is_active=True)

        response = admin_client.get(admin_book_list_url)

        results = response.data["results"]

        expected_fields = {
            "id",
            "name",
            "avatar",
            "price",
            "number_of_pages",
            "publication_date",
            "language",
            "inventory",
            "is_active",
            "created_at",
            "modified_at",
            "authors",
            "translators",
            "categories",
            "publisher",
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert set(results[0].keys()) == expected_fields

    def test_admin_book_list_returns_both_active_and_inactive_books(
        self,
        admin_client,
        book_factory,
        admin_book_list_url,
    ):
        book_factory(name="Active Book", is_active=True)
        book_factory(name="Inactive Book", is_active=False)

        response = admin_client.get(admin_book_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    # --------------------------------------------------------------------------
    # Default Ordering (-modified_at)
    # --------------------------------------------------------------------------
    def test_get_book_list_default_ordering_by_modified_at_descending(
        self, admin_client, book_factory, admin_book_list_url
    ):
        book1 = book_factory(name="First Created Book")
        book2 = book_factory(name="Second Created Book")

        # Update first book to have a more recent modified_at
        book1.name = "First Created Book Updated"
        book1.save()

        response = admin_client.get(admin_book_list_url)

        assert response.status_code == status.HTTP_200_OK
        results = response.data["results"]
        assert results[0]["id"] == book1.id
        assert results[1]["id"] == book2.id

    # --------------------------------------------------------------------------
    # Filters & Searching & Ordering
    # --------------------------------------------------------------------------
    def test_filter_book_list_by_is_active(self, admin_client, book_factory, admin_book_list_url):
        book_factory(name="Active Book", is_active=True)
        book_factory(name="Inactive Book", is_active=False)

        response_active = admin_client.get(admin_book_list_url, {"is_active": "true"})
        response_inactive = admin_client.get(admin_book_list_url, {"is_active": "false"})

        assert response_active.data["count"] == 1
        assert response_active.data["results"][0]["name"] == "Active Book"
        assert response_inactive.data["count"] == 1
        assert response_inactive.data["results"][0]["name"] == "Inactive Book"

    def test_book_list_search_by_name(self, admin_client, book_factory, admin_book_list_url):
        book_factory(name="Design Patterns")
        book_factory(name="Refactoring")

        response = admin_client.get(admin_book_list_url, {"search": "patterns"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Design Patterns"

    def test_get_books_list_search_by_name_is_case_insensitive(self, admin_client, book_factory, admin_book_list_url):
        book_factory(name="Clean Architecture")

        response_upper = admin_client.get(admin_book_list_url, {"search": "CLEAN"})
        response_lower = admin_client.get(admin_book_list_url, {"search": "clean"})

        assert response_upper.status_code == status.HTTP_200_OK
        assert response_upper.data["count"] == 1
        assert response_upper.data["results"][0]["name"] == "Clean Architecture"

        assert response_lower.status_code == status.HTTP_200_OK
        assert response_lower.data["count"] == 1
        assert response_lower.data["results"][0]["name"] == "Clean Architecture"

    def test_book_list_search_by_author_name(self, admin_client, book_factory, author_factory, admin_book_list_url):
        author = author_factory(name="Martin Fowler")
        book = book_factory(name="Refactoring")
        book.authors.add(author)

        book_factory(name="Clean Architecture")

        response = admin_client.get(admin_book_list_url, {"search": "fowler"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Refactoring"

    def test_get_books_list_search_by_author_name_is_case_insensitive(
        self, admin_client, book_factory, author_factory, admin_book_list_url
    ):
        author = author_factory(name="Robert C. Martin")
        book = book_factory(name="Clean Agile")
        book.authors.add(author)

        response_upper = admin_client.get(admin_book_list_url, {"search": "ROBERT"})
        response_lower = admin_client.get(admin_book_list_url, {"search": "robert"})

        assert response_upper.status_code == status.HTTP_200_OK
        assert response_upper.data["count"] == 1
        assert response_upper.data["results"][0]["name"] == "Clean Agile"

        assert response_lower.status_code == status.HTTP_200_OK
        assert response_lower.data["count"] == 1
        assert response_lower.data["results"][0]["name"] == "Clean Agile"

    def test_get_books_list_search_returns_empty_list_when_no_match(
        self, admin_client, book_factory, admin_book_list_url
    ):
        book_factory(name="Domain Driven Design")

        response = admin_client.get(admin_book_list_url, {"search": "NonExistentTermXYZ"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert response.data["results"] == []

    def test_order_book_list_by_id(self, admin_client, book_factory, admin_book_list_url):
        book_1 = book_factory(name="Alpha Book")
        book_2 = book_factory(name="Beta Book")

        response = admin_client.get(admin_book_list_url, {"ordering": "id"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_1.id
        assert results[1]["id"] == book_2.id

    def test_order_book_list_by_id_desc(self, admin_client, book_factory, admin_book_list_url):
        book_1 = book_factory(name="Alpha Book")
        book_2 = book_factory(name="Beta Book")

        response = admin_client.get(admin_book_list_url, {"ordering": "-id"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_2.id
        assert results[1]["id"] == book_1.id

    def test_order_book_list_by_price(self, admin_client, book_factory, admin_book_list_url):
        book_cheap = book_factory(name="Book Cheap", price=10000)
        book_expensive = book_factory(name="Book Expensive", price=90000)

        response = admin_client.get(admin_book_list_url, {"ordering": "price"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_cheap.id
        assert results[1]["id"] == book_expensive.id

    def test_order_book_list_by_price_desc(self, admin_client, book_factory, admin_book_list_url):
        book_cheap = book_factory(name="Book Cheap", price=10000)
        book_expensive = book_factory(name="Book Expensive", price=90000)

        response = admin_client.get(admin_book_list_url, {"ordering": "-price"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_expensive.id
        assert results[1]["id"] == book_cheap.id

    def test_order_book_list_by_publication_date(self, admin_client, book_factory, admin_book_list_url):
        book_old = book_factory(name="Old Book", publication_date="2000-01-01")
        book_new = book_factory(name="New Book", publication_date="2024-01-01")

        response = admin_client.get(admin_book_list_url, {"ordering": "publication_date"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_old.id
        assert results[1]["id"] == book_new.id

    def test_order_book_list_by_publication_date_desc(self, admin_client, book_factory, admin_book_list_url):
        book_old = book_factory(name="Old Book", publication_date="2000-01-01")
        book_new = book_factory(name="New Book", publication_date="2024-01-01")

        response = admin_client.get(admin_book_list_url, {"ordering": "-publication_date"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_new.id
        assert results[1]["id"] == book_old.id

    def test_order_book_list_by_created_at(self, admin_client, book_factory, admin_book_list_url):
        book_1 = book_factory(name="First Created")
        book_2 = book_factory(name="Second Created")

        response = admin_client.get(admin_book_list_url, {"ordering": "created_at"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_1.id
        assert results[1]["id"] == book_2.id

    def test_order_book_list_by_created_at_desc(self, admin_client, book_factory, admin_book_list_url):
        book_1 = book_factory(name="First Created")
        book_2 = book_factory(name="Second Created")

        response = admin_client.get(admin_book_list_url, {"ordering": "-created_at"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_2.id
        assert results[1]["id"] == book_1.id

    def test_order_book_list_by_modified_at(self, admin_client, book_factory, admin_book_list_url):
        book_1 = book_factory(name="Book 1")
        book_2 = book_factory(name="Book 2")

        book_1.price = 99999
        book_1.save()

        response = admin_client.get(admin_book_list_url, {"ordering": "modified_at"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_2.id
        assert results[1]["id"] == book_1.id

    def test_order_book_list_by_modified_at_desc(self, admin_client, book_factory, admin_book_list_url):
        book_1 = book_factory(name="Book 1")
        book_2 = book_factory(name="Book 2")

        book_1.price = 99999
        book_1.save()

        response = admin_client.get(admin_book_list_url, {"ordering": "-modified_at"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == book_1.id
        assert results[1]["id"] == book_2.id

    # --------------------------------------------------------------------------
    # Pagination
    # --------------------------------------------------------------------------
    def test_get_book_list_pagination_structure(self, admin_client, book_factory, admin_book_list_url):
        for i in range(25):
            book_factory(name=f"Admin Book {i}")

        response = admin_client.get(admin_book_list_url)

        expected_keys = {
            "count",
            "pages",
            "current_page",
            "page_size",
            "next",
            "previous",
            "results",
        }

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == expected_keys
        assert response.data["count"] == 25
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1
        assert response.data["page_size"] == 20
        assert response.data["next"] is not None
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 20

    def test_get_books_list_default_page_size(self, admin_client, book_factory, admin_book_list_url):
        for i in range(25):
            book_factory(name=f"Admin Book Page {i}")

        response = admin_client.get(admin_book_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 25
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_books_list_custom_page_size(self, admin_client, book_factory, admin_book_list_url):
        for i in range(15):
            book_factory(name=f"Admin Book Custom {i}")

        response = admin_client.get(admin_book_list_url, {"page_size": 10})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 15
        assert response.data["pages"] == 2

    def test_get_books_list_page_size_respects_max_limit(self, admin_client, book_factory, admin_book_list_url):
        for i in range(60):
            book_factory(name=f"Admin Book Max {i}")

        response = admin_client.get(admin_book_list_url, {"page_size": 100})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_books_list_next_link_exists_on_first_page(self, admin_client, book_factory, admin_book_list_url):
        for i in range(25):
            book_factory(name=f"Admin Book Next {i}")

        response = admin_client.get(admin_book_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_books_list_previous_link_exists_on_second_page(self, admin_client, book_factory, admin_book_list_url):
        for i in range(25):
            book_factory(name=f"Admin Book Prev {i}")

        response = admin_client.get(admin_book_list_url, {"page": 2})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["next"] is None
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    # --------------------------------------------------------------------------
    # Create (POST)
    # --------------------------------------------------------------------------
    def test_owner_can_create_book(self, owner_client, admin_book_list_url, book_payload):
        response = owner_client.post(admin_book_list_url, data=book_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(name="Clean Code").exists()

    def test_admin_can_create_book(self, admin_client, admin_book_list_url, book_payload):
        response = admin_client.post(admin_book_list_url, data=book_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(name="Clean Code").exists()

    def test_customer_cannot_create_book(self, customer_client, admin_book_list_url, book_payload):
        response = customer_client.post(admin_book_list_url, data=book_payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Book.objects.filter(name="Clean Code").exists()

    def test_anonymous_cannot_create_book(self, api_client, admin_book_list_url, book_payload):
        response = api_client.post(admin_book_list_url, data=book_payload)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        assert not Book.objects.filter(name="Clean Code").exists()

    def test_create_book_name_is_required(self, admin_client, admin_book_list_url, book_payload):
        del book_payload["name"]

        response = admin_client.post(admin_book_list_url, data=book_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_create_book_name_must_be_unique(self, admin_client, book_factory, admin_book_list_url, book_payload):
        book_factory(name="Clean Code")

        response = admin_client.post(admin_book_list_url, data=book_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data


@pytest.mark.django_db
class TestBookDetailApi:

    # --------------------------------------------------------------------------
    # Permissions (GET)
    # --------------------------------------------------------------------------
    def test_owner_can_get_book_detail(self, owner_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = owner_client.get(admin_book_detail_url(book.id))

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_book_detail(self, admin_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = admin_client.get(admin_book_detail_url(book.id))

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_book_detail(self, customer_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = customer_client.get(admin_book_detail_url(book.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_book_detail(self, api_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = api_client.get(admin_book_detail_url(book.id))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_book_detail_expected_fields(self, admin_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = admin_client.get(admin_book_detail_url(book.id))

        expected_fields = {
            "id",
            "name",
            "avatar",
            "price",
            "number_of_pages",
            "publication_date",
            "language",
            "inventory",
            "is_active",
            "created_at",
            "modified_at",
            "authors",
            "translators",
            "categories",
            "publisher",
        }

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == expected_fields
        assert response.data["id"] == book.id

    def test_get_book_detail_not_found(self, admin_client, admin_book_detail_url):

        response = admin_client.get(admin_book_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # --------------------------------------------------------------------------
    # Partial Update (PATCH)
    # --------------------------------------------------------------------------
    def test_owner_can_patch_book(self, owner_client, book_factory, admin_book_detail_url):
        book = book_factory(name="Original Name")

        response = owner_client.patch(admin_book_detail_url(book.id), data={"name": "Patched Name"})

        book.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert book.name == "Patched Name"

    def test_admin_can_patch_book(self, admin_client, book_factory, admin_book_detail_url):
        book = book_factory(name="Original Name")

        response = admin_client.patch(admin_book_detail_url(book.id), data={"name": "Patched by Admin"})

        book.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert book.name == "Patched by Admin"

    def test_customer_cannot_patch_book(self, customer_client, book_factory, admin_book_detail_url):
        book = book_factory(name="Original Name")

        response = customer_client.patch(admin_book_detail_url(book.id), data={"name": "Hacked Name"})

        book.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert book.name == "Original Name"

    # --------------------------------------------------------------------------
    # Full Update (PUT)
    # --------------------------------------------------------------------------
    def test_owner_can_put_book(self, owner_client, book_factory, admin_book_detail_url, book_payload):
        book = book_factory()

        book_payload["name"] = "Full Updated Name"
        response = owner_client.put(admin_book_detail_url(book.id), data=book_payload)

        book.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert book.name == "Full Updated Name"

    def test_admin_can_put_book(self, admin_client, book_factory, admin_book_detail_url, book_payload):
        book = book_factory()

        book_payload["name"] = "Full Updated by Admin"
        response = admin_client.put(admin_book_detail_url(book.id), data=book_payload)

        book.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert book.name == "Full Updated by Admin"

    def test_customer_cannot_put_book(self, customer_client, book_factory, admin_book_detail_url, book_payload):
        book = book_factory(name="Safe Name")

        response = customer_client.put(admin_book_detail_url(book.id))

        book.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert book.name == "Safe Name"

    def test_put_book_name_is_required(self, admin_client, book_factory, admin_book_detail_url, book_payload):
        book = book_factory()
        del book_payload["name"]

        response = admin_client.put(admin_book_detail_url(book.id), data=book_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_put_book_name_must_be_unique(self, admin_client, book_factory, admin_book_detail_url, book_payload):
        book_factory(name="Existing Book")
        book = book_factory(name="Book To Edit")

        book_payload["name"] = "Existing Book"
        response = admin_client.put(admin_book_detail_url(book.id), data=book_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_put_read_only_fields_are_ignored(self, admin_client, book_factory, admin_book_detail_url, book_payload):
        book = book_factory()
        original_id = book.id
        original_created_at = book.created_at

        tampered_payload = book_payload.copy()
        tampered_payload["id"] = 99999
        tampered_payload["created_at"] = "2020-01-01T00:00:00Z"

        response = admin_client.put(admin_book_detail_url(book.id), data=tampered_payload)

        book.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert book.id == original_id
        assert book.created_at == original_created_at

    # --------------------------------------------------------------------------
    # Delete (DELETE) - Strict Permission Matrix
    # --------------------------------------------------------------------------
    def test_owner_can_delete_book(self, owner_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = owner_client.delete(admin_book_detail_url(book.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Book.objects.filter(id=book.id).exists()

    def test_admin_cannot_delete_book(self, admin_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = admin_client.delete(admin_book_detail_url(book.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Book.objects.filter(id=book.id).exists()

    def test_customer_cannot_delete_book(self, customer_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = customer_client.delete(admin_book_detail_url(book.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Book.objects.filter(id=book.id).exists()

    def test_anonymous_cannot_delete_book(self, api_client, book_factory, admin_book_detail_url):
        book = book_factory()

        response = api_client.delete(admin_book_detail_url(book.id))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        assert Book.objects.filter(id=book.id).exists()
