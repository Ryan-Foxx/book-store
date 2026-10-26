import pytest
from apps.books.models import Comment
from rest_framework import status

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def comment_payload():
    return {"body": "This is an insightful book! Highly recommended."}


@pytest.mark.django_db
class TestCommentListAndCreateApi:
    """Test suite for public nested Comment List and Create API endpoints."""

    # --------------------------------------------------------------------------
    # List Comments (GET)
    # --------------------------------------------------------------------------
    def test_get_approved_comments_list(self, api_client, book_factory, comment_factory, public_comment_list_url):
        book = book_factory(is_active=True)
        # Create approved and waiting/rejected comments
        comment_factory(book=book, body="Approved Comment 1", status=Comment.COMMENT_STATUS_APPROVED)
        comment_factory(book=book, body="Approved Comment 2", status=Comment.COMMENT_STATUS_APPROVED)
        comment_factory(book=book, body="Waiting Comment", status=Comment.COMMENT_STATUS_WAITING)

        url = public_comment_list_url(book.id)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        results = response.data["results"]
        # Only approved comments should be listed
        assert response.data["count"] == 2
        bodies = [c["body"] for c in results]
        assert "Approved Comment 1" in bodies
        assert "Approved Comment 2" in bodies
        assert "Waiting Comment" not in bodies

    def test_get_comment_list_ordered_by_created_at_desc(
        self, api_client, book_factory, comment_factory, public_comment_list_url
    ):
        book = book_factory(is_active=True)
        c1 = comment_factory(book=book, body="First Comment", status=Comment.COMMENT_STATUS_APPROVED)
        c2 = comment_factory(book=book, body="Second Comment", status=Comment.COMMENT_STATUS_APPROVED)

        url = public_comment_list_url(book.id)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        results = response.data["results"]
        # Descending order: newest first
        assert results[0]["id"] == c2.id
        assert results[1]["id"] == c1.id

    def test_get_comment_list_expected_fields(self, api_client, book_factory, comment_factory, public_comment_list_url):
        book = book_factory(is_active=True)
        comment_factory(book=book, status=Comment.COMMENT_STATUS_APPROVED)

        url = public_comment_list_url(book.id)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        results = response.data["results"]
        assert len(results) == 1

        expected_fields = {"id", "username", "avatar", "body", "created_at"}
        assert set(results[0].keys()) == expected_fields

    def test_get_comment_list_for_inactive_book_returns_empty(
        self, api_client, book_factory, comment_factory, public_comment_list_url
    ):
        inactive_book = book_factory(is_active=False)
        comment_factory(book=inactive_book, status=Comment.COMMENT_STATUS_APPROVED)

        url = public_comment_list_url(inactive_book.id)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert response.data["results"] == []

    def test_get_comment_list_invalid_book_id_raises_validation_error(self, api_client, public_comment_list_url):
        url = public_comment_list_url("invalid-id-string")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data

    # --------------------------------------------------------------------------
    # Pagination (CommentPagination: page_size = 10)
    # --------------------------------------------------------------------------
    def test_comment_list_pagination_structure_and_default_size(
        self, api_client, book_factory, comment_factory, public_comment_list_url
    ):
        book = book_factory(is_active=True)
        for i in range(15):
            comment_factory(book=book, body=f"Comment {i}", status=Comment.COMMENT_STATUS_APPROVED)

        url = public_comment_list_url(book.id)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 15
        assert response.data["page_size"] == 10
        assert len(response.data["results"]) == 10
        assert response.data["next"] is not None
        assert "page=2" in response.data["next"]

    # --------------------------------------------------------------------------
    # Create Comments (POST)
    # --------------------------------------------------------------------------
    def test_authenticated_user_can_create_comment(
        self, customer_client, book_factory, public_comment_list_url, comment_payload
    ):
        book = book_factory(is_active=True)
        url = public_comment_list_url(book.id)

        response = customer_client.post(url, data=comment_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.filter(book=book, body=comment_payload["body"]).exists()

    def test_anonymous_user_cannot_create_comment(
        self, api_client, book_factory, public_comment_list_url, comment_payload
    ):
        book = book_factory(is_active=True)
        url = public_comment_list_url(book.id)

        response = api_client.post(url, data=comment_payload)

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        assert not Comment.objects.filter(body=comment_payload["body"]).exists()

    def test_create_comment_on_inactive_book_fails(
        self, customer_client, book_factory, public_comment_list_url, comment_payload
    ):
        inactive_book = book_factory(is_active=False)
        url = public_comment_list_url(inactive_book.id)

        response = customer_client.post(url, data=comment_payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert not Comment.objects.filter(body=comment_payload["body"]).exists()

    def test_create_comment_with_invalid_book_id_fails(self, customer_client, public_comment_list_url, comment_payload):
        url = public_comment_list_url("abc-not-integer")

        response = customer_client.post(url, data=comment_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "book_id" in response.data

    def test_create_comment_body_is_required(self, customer_client, book_factory, public_comment_list_url):
        book = book_factory(is_active=True)
        url = public_comment_list_url(book.id)

        response = customer_client.post(url, data={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "body" in response.data
