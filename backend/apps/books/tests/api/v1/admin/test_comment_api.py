import pytest
from apps.books.models import Comment
from rest_framework import status

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def comment_payload(user_factory, book_factory):
    user = user_factory()
    book = book_factory()

    return {
        "user": user.id,
        "book": book.id,
        "body": "This is a great book, highly recommended!",
        "status": Comment.COMMENT_STATUS_APPROVED,
    }


@pytest.mark.django_db
class TestCommentListApi:

    # --------------------------------------------------------------------------
    # Permissions
    # --------------------------------------------------------------------------
    def test_owner_can_get_comment_list(self, owner_client, admin_comment_list_url):
        response = owner_client.get(admin_comment_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_comment_list(self, admin_client, admin_comment_list_url):
        response = admin_client.get(admin_comment_list_url)

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_comment_list(self, customer_client, admin_comment_list_url):
        response = customer_client.get(admin_comment_list_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_comment_list(self, api_client, admin_comment_list_url):
        response = api_client.get(admin_comment_list_url)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    # --------------------------------------------------------------------------
    # Response Structure
    # --------------------------------------------------------------------------
    def test_get_comment_list_expected_fields(self, admin_client, comment_factory, admin_comment_list_url):
        comment_factory(body="Sample comment body")

        response = admin_client.get(admin_comment_list_url)

        results = response.data["results"]

        expected_fields = {
            "id",
            "username",
            "avatar",
            "book",
            "body",
            "status",
            "created_at",
            "modified_at",
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert set(results[0].keys()) == expected_fields

    # --------------------------------------------------------------------------
    # Default Ordering (-modified_at)
    # --------------------------------------------------------------------------
    def test_get_comment_list_default_ordering_by_modified_at_descending(
        self, admin_client, comment_factory, admin_comment_list_url
    ):
        comment1 = comment_factory(body="First Created Comment")
        comment2 = comment_factory(body="Second Created Comment")

        # Update first comment to have a more recent modified_at
        comment1.body = "First Created Comment Updated"
        comment1.save()

        response = admin_client.get(admin_comment_list_url)

        assert response.status_code == status.HTTP_200_OK
        results = response.data["results"]
        assert results[0]["id"] == comment1.id
        assert results[1]["id"] == comment2.id

    # --------------------------------------------------------------------------
    # Filters & Searching & Ordering
    # --------------------------------------------------------------------------
    def test_comment_list_search_by_username(self, admin_client, comment_factory, user_factory, admin_comment_list_url):
        user_alice = user_factory(username="alice")
        user_bob = user_factory(username="bob")

        comment_factory(user=user_alice, body="Comment by Alice")
        comment_factory(user=user_bob, body="Comment by Bob")

        response = admin_client.get(admin_comment_list_url, {"search": "alice"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["username"] == "alice"

    def test_get_comments_list_search_by_username_is_case_insensitive(
        self, admin_client, comment_factory, user_factory, admin_comment_list_url
    ):
        user = user_factory(username="alice_smith")
        comment_factory(user=user)

        response_upper = admin_client.get(admin_comment_list_url, {"search": "ALICE"})
        response_lower = admin_client.get(admin_comment_list_url, {"search": "alice"})

        assert response_upper.status_code == status.HTTP_200_OK
        assert response_upper.data["count"] == 1
        assert response_upper.data["results"][0]["username"] == "alice_smith"

        assert response_lower.status_code == status.HTTP_200_OK
        assert response_lower.data["count"] == 1
        assert response_lower.data["results"][0]["username"] == "alice_smith"

    def test_comment_list_search_by_book_name(
        self, admin_client, comment_factory, book_factory, admin_comment_list_url
    ):
        book_clean = book_factory(name="Clean Architecture")
        book_refactor = book_factory(name="Refactoring")

        comment_factory(book=book_clean, body="Great architecture tips")
        comment_factory(book=book_refactor, body="Nice refactoring patterns")

        response = admin_client.get(admin_comment_list_url, {"search": "Architecture"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["book"] == "Clean Architecture"

    def test_get_comments_list_search_by_book_name_is_case_insensitive(
        self, admin_client, comment_factory, book_factory, admin_comment_list_url
    ):
        book = book_factory(name="Clean Architecture")
        comment_factory(book=book)

        response_upper = admin_client.get(admin_comment_list_url, {"search": "CLEAN"})
        response_lower = admin_client.get(admin_comment_list_url, {"search": "clean"})

        assert response_upper.status_code == status.HTTP_200_OK
        assert response_upper.data["count"] == 1
        assert response_upper.data["results"][0]["book"] == "Clean Architecture"

        assert response_lower.status_code == status.HTTP_200_OK
        assert response_lower.data["count"] == 1
        assert response_lower.data["results"][0]["book"] == "Clean Architecture"

    def test_get_comments_list_search_returns_empty_list_when_no_match(
        self, admin_client, comment_factory, admin_comment_list_url
    ):
        comment_factory(body="Nice Book")

        response = admin_client.get(admin_comment_list_url, {"search": "NonExistentKeywordXYZ"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert response.data["results"] == []

    def test_order_comment_list_by_id(self, admin_client, comment_factory, admin_comment_list_url):
        comment_1 = comment_factory(body="Alpha Comment")
        comment_2 = comment_factory(body="Beta Comment")

        response = admin_client.get(admin_comment_list_url, {"ordering": "id"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_1.id
        assert results[1]["id"] == comment_2.id

    def test_order_comment_list_by_id_desc(self, admin_client, comment_factory, admin_comment_list_url):
        comment_1 = comment_factory(body="Alpha Comment")
        comment_2 = comment_factory(body="Beta Comment")

        response = admin_client.get(admin_comment_list_url, {"ordering": "-id"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_2.id
        assert results[1]["id"] == comment_1.id

    def test_order_comment_list_by_username(self, admin_client, comment_factory, user_factory, admin_comment_list_url):
        user_alice = user_factory(username="alice")
        user_bob = user_factory(username="bob")

        comment_alice = comment_factory(user=user_alice)
        comment_bob = comment_factory(user=user_bob)

        response = admin_client.get(admin_comment_list_url, {"ordering": "username"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_alice.id
        assert results[1]["id"] == comment_bob.id

    def test_order_comment_list_by_username_desc(
        self, admin_client, comment_factory, user_factory, admin_comment_list_url
    ):
        user_alice = user_factory(username="alice")
        user_bob = user_factory(username="bob")

        comment_alice = comment_factory(user=user_alice)
        comment_bob = comment_factory(user=user_bob)

        response = admin_client.get(admin_comment_list_url, {"ordering": "-username"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_bob.id
        assert results[1]["id"] == comment_alice.id

    def test_order_comment_list_by_book(self, admin_client, comment_factory, book_factory, admin_comment_list_url):
        book_alpha = book_factory(name="Alpha Book")
        book_beta = book_factory(name="Beta Book")

        comment_alpha = comment_factory(book=book_alpha)
        comment_beta = comment_factory(book=book_beta)

        response = admin_client.get(admin_comment_list_url, {"ordering": "book"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_alpha.id
        assert results[1]["id"] == comment_beta.id

    def test_order_comment_list_by_book_desc(self, admin_client, comment_factory, book_factory, admin_comment_list_url):
        book_alpha = book_factory(name="Alpha Book")
        book_beta = book_factory(name="Beta Book")

        comment_alpha = comment_factory(book=book_alpha)
        comment_beta = comment_factory(book=book_beta)

        response = admin_client.get(admin_comment_list_url, {"ordering": "-book"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_beta.id
        assert results[1]["id"] == comment_alpha.id

    def test_order_comment_list_by_created_at(self, admin_client, comment_factory, admin_comment_list_url):
        comment_1 = comment_factory(body="First Comment")
        comment_2 = comment_factory(body="Second Comment")

        response = admin_client.get(admin_comment_list_url, {"ordering": "created_at"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_1.id
        assert results[1]["id"] == comment_2.id

    def test_order_comment_list_by_created_at_desc(self, admin_client, comment_factory, admin_comment_list_url):
        comment_1 = comment_factory(body="First Comment")
        comment_2 = comment_factory(body="Second Comment")

        response = admin_client.get(admin_comment_list_url, {"ordering": "-created_at"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_2.id
        assert results[1]["id"] == comment_1.id

    def test_order_comment_list_by_modified_at(self, admin_client, comment_factory, admin_comment_list_url):
        comment_1 = comment_factory(body="Comment 1")
        comment_2 = comment_factory(body="Comment 2")

        comment_1.body = "Comment 1 Modified"
        comment_1.save()

        response = admin_client.get(admin_comment_list_url, {"ordering": "modified_at"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_2.id
        assert results[1]["id"] == comment_1.id

    def test_order_comment_list_by_modified_at_desc(self, admin_client, comment_factory, admin_comment_list_url):
        comment_1 = comment_factory(body="Comment 1")
        comment_2 = comment_factory(body="Comment 2")

        comment_1.body = "Comment 1 Modified"
        comment_1.save()

        response = admin_client.get(admin_comment_list_url, {"ordering": "-modified_at"})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["id"] == comment_1.id
        assert results[1]["id"] == comment_2.id

    # --------------------------------------------------------------------------
    # Pagination
    # --------------------------------------------------------------------------
    def test_get_comment_list_pagination_structure(self, admin_client, comment_factory, admin_comment_list_url):
        for i in range(25):
            comment_factory(body=f"Admin Comment {i}")

        response = admin_client.get(admin_comment_list_url)

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

    def test_get_comments_list_default_page_size(self, admin_client, comment_factory, admin_comment_list_url):
        for i in range(25):
            comment_factory(body=f"Admin Comment Page {i}")

        response = admin_client.get(admin_comment_list_url)

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 20
        assert response.data["page_size"] == 20
        assert response.data["count"] == 25
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1

    def test_get_comments_list_custom_page_size(self, admin_client, comment_factory, admin_comment_list_url):
        for i in range(15):
            comment_factory(body=f"Admin Comment Custom {i}")

        response = admin_client.get(admin_comment_list_url, {"page_size": 10})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 10
        assert response.data["page_size"] == 10
        assert response.data["count"] == 15
        assert response.data["pages"] == 2

    def test_get_comments_list_page_size_respects_max_limit(
        self, admin_client, comment_factory, admin_comment_list_url
    ):
        for i in range(60):
            comment_factory(body=f"Admin Comment Max {i}")

        response = admin_client.get(admin_comment_list_url, {"page_size": 100})

        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 50
        assert response.data["page_size"] == 50
        assert response.data["count"] == 60
        assert response.data["pages"] == 2

    def test_get_comments_list_next_link_exists_on_first_page(
        self, admin_client, comment_factory, admin_comment_list_url
    ):
        for i in range(25):
            comment_factory(body=f"Admin Comment Next {i}")

        response = admin_client.get(admin_comment_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]
        assert response.data["previous"] is None

    def test_get_comments_list_previous_link_exists_on_second_page(
        self, admin_client, comment_factory, admin_comment_list_url
    ):
        for i in range(25):
            comment_factory(body=f"Admin Comment Prev {i}")

        response = admin_client.get(admin_comment_list_url, {"page": 2})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["next"] is None
        assert response.data["previous"] is not None
        assert "page=1" in response.data["previous"]

    # --------------------------------------------------------------------------
    # Create (POST)
    # --------------------------------------------------------------------------
    def test_owner_can_create_comment(self, owner_client, admin_comment_list_url, comment_payload):
        response = owner_client.post(admin_comment_list_url, data=comment_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.filter(body=comment_payload["body"]).exists()

    def test_admin_can_create_comment(self, admin_client, admin_comment_list_url, comment_payload):
        response = admin_client.post(admin_comment_list_url, data=comment_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.filter(body=comment_payload["body"]).exists()

    def test_customer_cannot_create_comment(self, customer_client, admin_comment_list_url, comment_payload):
        response = customer_client.post(admin_comment_list_url, data=comment_payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Comment.objects.filter(body=comment_payload["body"]).exists()

    def test_anonymous_cannot_create_comment(self, api_client, admin_comment_list_url, comment_payload):
        response = api_client.post(admin_comment_list_url, data=comment_payload)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        assert not Comment.objects.filter(body=comment_payload["body"]).exists()

    def test_create_comment_body_is_required(self, admin_client, admin_comment_list_url, comment_payload):
        del comment_payload["body"]

        response = admin_client.post(admin_comment_list_url, data=comment_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "body" in response.data

    def test_create_comment_user_is_required(self, admin_client, admin_comment_list_url, comment_payload):
        del comment_payload["user"]

        response = admin_client.post(admin_comment_list_url, data=comment_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "user" in response.data

    def test_create_comment_book_is_required(self, admin_client, admin_comment_list_url, comment_payload):
        del comment_payload["book"]

        response = admin_client.post(admin_comment_list_url, data=comment_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "book" in response.data


@pytest.mark.django_db
class TestCommentDetailApi:

    # --------------------------------------------------------------------------
    # Permissions
    # --------------------------------------------------------------------------
    def test_owner_can_get_comment_detail(self, owner_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = owner_client.get(admin_comment_detail_url(comment.id))

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_get_comment_detail(self, admin_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = admin_client.get(admin_comment_detail_url(comment.id))

        assert response.status_code == status.HTTP_200_OK

    def test_customer_cannot_get_comment_detail(self, customer_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = customer_client.get(admin_comment_detail_url(comment.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_cannot_get_comment_detail(self, api_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = api_client.get(admin_comment_detail_url(comment.id))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_comment_detail_expected_fields(self, admin_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = admin_client.get(admin_comment_detail_url(comment.id))

        expected_fields = {
            "id",
            "username",
            "avatar",
            "book",
            "body",
            "status",
            "created_at",
            "modified_at",
        }

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == expected_fields
        assert response.data["id"] == comment.id

    def test_get_comment_detail_not_found(self, admin_client, admin_comment_detail_url):
        response = admin_client.get(admin_comment_detail_url(999999))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # --------------------------------------------------------------------------
    # Partial Update (PATCH)
    # --------------------------------------------------------------------------
    def test_owner_can_patch_comment(self, owner_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory(body="Original Comment")

        response = owner_client.patch(
            admin_comment_detail_url(comment.id),
            data={"body": "Patched Comment by Owner", "status": Comment.COMMENT_STATUS_APPROVED},
        )

        comment.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert comment.body == "Patched Comment by Owner"
        assert comment.status == Comment.COMMENT_STATUS_APPROVED

    def test_admin_can_patch_comment(self, admin_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory(body="Original Comment")

        response = admin_client.patch(
            admin_comment_detail_url(comment.id),
            data={"body": "Patched Comment by Admin", "status": Comment.COMMENT_STATUS_NOT_APPROVED},
        )

        comment.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert comment.body == "Patched Comment by Admin"
        assert comment.status == Comment.COMMENT_STATUS_NOT_APPROVED

    def test_customer_cannot_patch_comment(self, customer_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory(body="Original Comment")

        response = customer_client.patch(admin_comment_detail_url(comment.id), data={"body": "Hacked Comment"})

        comment.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert comment.body == "Original Comment"

    # --------------------------------------------------------------------------
    # Full Update (PUT)
    # --------------------------------------------------------------------------
    def test_owner_can_put_comment(self, owner_client, comment_factory, admin_comment_detail_url, comment_payload):
        comment = comment_factory()

        comment_payload["body"] = "Full Updated Body by Owner"
        response = owner_client.put(admin_comment_detail_url(comment.id), data=comment_payload)

        comment.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert comment.body == "Full Updated Body by Owner"

    def test_admin_can_put_comment(self, admin_client, comment_factory, admin_comment_detail_url, comment_payload):
        comment = comment_factory()

        comment_payload["body"] = "Full Updated Body by Admin"
        response = admin_client.put(admin_comment_detail_url(comment.id), data=comment_payload)

        comment.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert comment.body == "Full Updated Body by Admin"

    def test_customer_cannot_put_comment(
        self, customer_client, comment_factory, admin_comment_detail_url, comment_payload
    ):
        comment = comment_factory(body="Safe Comment")

        response = customer_client.put(admin_comment_detail_url(comment.id), data=comment_payload)

        comment.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert comment.body == "Safe Comment"

    def test_put_comment_body_is_required(
        self, admin_client, comment_factory, admin_comment_detail_url, comment_payload
    ):
        comment = comment_factory()
        del comment_payload["body"]

        response = admin_client.put(admin_comment_detail_url(comment.id), data=comment_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "body" in response.data

    def test_put_read_only_fields_are_ignored(
        self, admin_client, comment_factory, admin_comment_detail_url, comment_payload
    ):
        comment = comment_factory()
        original_id = comment.id
        original_created_at = comment.created_at

        tampered_payload = comment_payload.copy()
        tampered_payload["id"] = 99999
        tampered_payload["created_at"] = "2020-01-01T00:00:00Z"

        response = admin_client.put(admin_comment_detail_url(comment.id), data=tampered_payload)

        comment.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert comment.id == original_id
        assert comment.created_at == original_created_at

    # --------------------------------------------------------------------------
    # Delete (DELETE) - Strict Permission Matrix
    # --------------------------------------------------------------------------
    def test_owner_can_delete_comment(self, owner_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = owner_client.delete(admin_comment_detail_url(comment.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=comment.id).exists()

    def test_admin_cannot_delete_comment(self, admin_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = admin_client.delete(admin_comment_detail_url(comment.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Comment.objects.filter(id=comment.id).exists()

    def test_customer_cannot_delete_comment(self, customer_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = customer_client.delete(admin_comment_detail_url(comment.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Comment.objects.filter(id=comment.id).exists()

    def test_anonymous_cannot_delete_comment(self, api_client, comment_factory, admin_comment_detail_url):
        comment = comment_factory()

        response = api_client.delete(admin_comment_detail_url(comment.id))

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        assert Comment.objects.filter(id=comment.id).exists()
