import pytest
from apps.users.models import User
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUsersAPI:

    @pytest.fixture(autouse=True)
    def setup_urls(self):
        # Reverse resolve Djoser user endpoints registered under 'custom-user' basename
        self.user_create_url = reverse("custom-user-list")  # POST /api/v1/auth/users/
        self.user_list_url = reverse("custom-user-list")  # GET /api/v1/auth/users/ (disabled)

    def test_user_registration_successful(self, api_client, settings):
        # Override Djoser settings to disable activation email during test execution
        settings.DJOSER = {**settings.DJOSER, "SEND_ACTIVATION_EMAIL": False}

        payload = {
            "username": "newapiuser",
            "password": "StrongPassword123!",
            "email": "newapiuser@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "phone_number": "09129876543",
        }

        response = api_client.post(self.user_create_url, data=payload, format="json")
        data = response.data

        assert response.status_code == status.HTTP_201_CREATED
        assert data["username"] == "newapiuser"
        assert data["email"] == "newapiuser@example.com"
        assert "id" in data
        # Password must never be leaked in serializer representation
        assert "password" not in data

        # Verify user is successfully created in the database and phone is normalized to E.164
        user = User.objects.get(username="newapiuser")
        assert user.phone_number == "+989129876543"
        # Role must always default to customer
        assert user.role == User.ROLE_CHOICE_CUSTOMER

    def test_user_registration_invalid_phone_number_fails(self, api_client, settings):
        settings.DJOSER = {**settings.DJOSER, "SEND_ACTIVATION_EMAIL": False}

        payload = {
            "username": "badphoneuser",
            "password": "StrongPassword123!",
            "email": "badphone@example.com",
            "phone_number": "02112345678",  # Invalid Iranian mobile prefix (Tehran landline)
        }

        response = api_client.post(self.user_create_url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "phone_number" in response.data

    def test_disabled_user_list_endpoint_returns_404(self, api_client, customer_user):
        # Authenticate first to pass Djoser default permissions and hit the custom 404 handler
        api_client.force_authenticate(user=customer_user)

        # CustomUserViewSet explicitly disables GET /users/ list view
        response = api_client.get(self.user_list_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_disabled_user_me_endpoint_returns_404(self, api_client, customer_user):
        # CustomUserViewSet explicitly disables /users/me/ action endpoint
        api_client.force_authenticate(user=customer_user)
        me_url = reverse("custom-user-me")

        response = api_client.get(me_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
