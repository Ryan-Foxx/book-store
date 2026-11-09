import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestLogoutAPI:

    @pytest.fixture(autouse=True)
    def setup_url(self):
        # Reverse resolve the logout endpoint route
        self.logout_url = reverse("logout")

    def test_logout_successful_returns_205_and_blacklists_token(self, api_client, customer_user):
        # Generate valid refresh token for the authenticated user
        refresh = RefreshToken.for_user(customer_user)
        api_client.force_authenticate(user=customer_user)

        payload = {"refresh": str(refresh)}
        response = api_client.post(self.logout_url, data=payload, format="json")

        # Verify response code and response structure
        assert response.status_code == status.HTTP_205_RESET_CONTENT
        assert response.data == {"detail": "Successfully logged out."}

        # Verify that the token is blacklisted in the database table
        assert BlacklistedToken.objects.filter(token__token=str(refresh)).exists()

    def test_logout_idempotent_when_token_already_blacklisted(self, api_client, customer_user):
        refresh = RefreshToken.for_user(customer_user)
        api_client.force_authenticate(user=customer_user)

        payload = {"refresh": str(refresh)}

        # First request successfully blacklists the token
        first_resp = api_client.post(self.logout_url, data=payload, format="json")
        assert first_resp.status_code == status.HTTP_205_RESET_CONTENT

        # Second request with the same blacklisted token is rejected with 400 Bad Request
        # because simplejwt validation catches blacklisted tokens upfront.
        second_resp = api_client.post(self.logout_url, data=payload, format="json")
        assert second_resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "refresh" in second_resp.data

    def test_logout_unauthenticated_request_fails(self, api_client, customer_user):
        refresh = RefreshToken.for_user(customer_user)

        # Send request without authenticating the client
        payload = {"refresh": str(refresh)}
        response = api_client.post(self.logout_url, data=payload, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_missing_refresh_token_fails(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)

        # Empty payload
        response = api_client.post(self.logout_url, data={}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "refresh" in response.data

    def test_logout_invalid_refresh_token_string_fails(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)

        payload = {"refresh": "not-a-valid-jwt-token"}
        response = api_client.post(self.logout_url, data=payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "refresh" in response.data

    def test_logout_token_ownership_mismatch_fails(self, api_client, user_factory):
        # Create two distinct users
        user_owner = user_factory(username="token_owner")
        user_attacker = user_factory(username="attacker")

        # Generate token for user_owner, but authenticate as user_attacker
        refresh = RefreshToken.for_user(user_owner)
        api_client.force_authenticate(user=user_attacker)

        payload = {"refresh": str(refresh)}
        response = api_client.post(self.logout_url, data=payload, format="json")

        # Cross-user logout attempt must be rejected
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get("detail") == "This token does not belong to the authenticated user."
