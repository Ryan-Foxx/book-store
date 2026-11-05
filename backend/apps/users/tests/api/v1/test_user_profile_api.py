import pytest
from apps.users.models import UserProfile
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserProfileAPI:

    @pytest.fixture(autouse=True)
    def setup_url(self):
        # Reverse resolve the profile endpoint route (/api/v1/auth/profile/me/)
        self.profile_url = reverse("user-profile")

    def test_get_user_profile_successful(self, api_client, customer_user):
        # Authenticate client as customer_user (profile is auto-created by post_save signal)
        api_client.force_authenticate(user=customer_user)

        response = api_client.get(self.profile_url)
        data = response.data

        assert response.status_code == status.HTTP_200_OK
        # Verify top-level profile fields and nested user representation
        assert data["id"] == customer_user.profile.id
        assert data["user"]["username"] == customer_user.username
        assert data["user"]["email"] == customer_user.email
        assert data["user"]["role"] == customer_user.role
        assert "avatar" in data

    def test_get_user_profile_unauthenticated_fails(self, api_client):
        # Request without authentication token should be rejected with 401
        response = api_client.get(self.profile_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_user_profile_not_found_returns_404(self, api_client, customer_user):
        # Explicitly delete the auto-created profile to trigger NotFound (404)
        UserProfile.objects.filter(user=customer_user).delete()
        customer_user.refresh_from_db()

        api_client.force_authenticate(user=customer_user)

        response = api_client.get(self.profile_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Profile not found for this user."

    def test_patch_user_profile_updates_allowed_fields(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)

        payload = {
            "user": {
                "first_name": "UpdatedFirst",
                "last_name": "UpdatedLast",
            }
        }

        response = api_client.patch(self.profile_url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK

        # Refresh user instance from database to verify changes
        customer_user.refresh_from_db()
        assert customer_user.first_name == "UpdatedFirst"
        assert customer_user.last_name == "UpdatedLast"

    def test_patch_user_profile_ignores_read_only_nested_fields(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)

        original_email = customer_user.email
        original_role = customer_user.role

        # Attempt to inject unauthorized updates on read-only fields
        payload = {
            "user": {
                "first_name": "NewName",
                "email": "malicious@example.com",
                "role": "owner",
            }
        }

        response = api_client.patch(self.profile_url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK

        customer_user.refresh_from_db()
        # Allowed field should change, read-only fields must remain untouched
        assert customer_user.first_name == "NewName"
        assert customer_user.email == original_email
        assert customer_user.role == original_role

    def test_put_user_profile_skips_empty_nested_user(self, api_client, customer_user):
        api_client.force_authenticate(user=customer_user)

        customer_user.first_name = "Original"
        customer_user.save()

        # PUT payload omitting or passing empty nested user data should succeed without clearing user fields
        payload = {"user": {}}

        response = api_client.put(self.profile_url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK

        customer_user.refresh_from_db()
        assert customer_user.first_name == "Original"
