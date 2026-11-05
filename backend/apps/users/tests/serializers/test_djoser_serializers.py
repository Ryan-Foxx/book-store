import pytest
from apps.users.api.v1.serializers.djoser_serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


@pytest.mark.django_db
class TestUserCreateSerializer:

    def test_user_create_serializer_successful(self):
        # Prepare valid payload with a standard zero-prefixed Iranian mobile number
        data = {
            "username": "testuser1",
            "password": "StrongPassword123!",
            "email": "test1@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "09123456789",
        }
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        assert user.username == "testuser1"
        assert user.email == "test1@example.com"
        # Verify that the phone number is normalized to E.164 format
        assert user.phone_number == "+989123456789"
        assert user.check_password("StrongPassword123!") is True

    def test_user_create_serializer_normalizes_various_phone_formats(self):
        # Test international country code format without leading '+'
        data = {
            "username": "testuser2",
            "password": "StrongPassword123!",
            "email": "test2@example.com",
            "phone_number": "989129876543",
        }
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        assert user.phone_number == "+989129876543"

    def test_user_create_serializer_invalid_phone_number(self):
        # Iranian landline or invalid pattern should fail validation
        data = {
            "username": "testuser3",
            "password": "StrongPassword123!",
            "email": "test3@example.com",
            "phone_number": "02112345678",
        }
        serializer = UserCreateSerializer(data=data)

        assert not serializer.is_valid()
        assert "phone_number" in serializer.errors

    def test_user_create_serializer_duplicate_phone_number(self):
        # Create an existing user with normalized phone number in the database
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            phone_number="+989121112233",
            password="Password123!",
        )

        # Attempt to register another account with the raw equivalent phone number
        data = {
            "username": "newuser",
            "password": "StrongPassword123!",
            "email": "new@example.com",
            "phone_number": "09121112233",
        }
        serializer = UserCreateSerializer(data=data)

        # Catch duplicate either during serializer validation or model save/full_clean
        if serializer.is_valid():
            with pytest.raises((Exception, DjangoValidationError)):
                serializer.save()
        else:
            assert "phone_number" in serializer.errors
