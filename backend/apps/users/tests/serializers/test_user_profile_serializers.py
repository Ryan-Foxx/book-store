import pytest
from apps.users.api.v1.serializers.user_profile_serializers import UserProfileSerializer


@pytest.mark.django_db
class TestUserProfileSerializer:

    def test_user_profile_serializer_read(self, user_factory):
        user = user_factory(
            username="profileuser",
            email="profile@example.com",
            first_name="Alice",
            last_name="Smith",
            role="customer",
        )
        # Profile is automatically instantiated by post_save signal
        profile = user.profile

        serializer = UserProfileSerializer(instance=profile)
        data = serializer.data

        # Verify integer primary key and nested user representation
        assert data["id"] == profile.id
        assert data["user"]["username"] == "profileuser"
        assert data["user"]["email"] == "profile@example.com"
        assert data["user"]["first_name"] == "Alice"
        assert data["user"]["role"] == "customer"

    def test_user_profile_serializer_update_nested_user_fields(self, user_factory):
        user = user_factory(first_name="OldFirst", last_name="OldLast")
        profile = user.profile

        payload = {
            "user": {
                "first_name": "NewFirst",
                "last_name": "NewLast",
                # The following fields are read-only and must be ignored
                "email": "hacker@example.com",
                "role": "owner",
            }
        }

        serializer = UserProfileSerializer(instance=profile, data=payload, partial=True)
        assert serializer.is_valid(), serializer.errors

        serializer.save()

        # Reload user from DB to confirm allowable updates and read-only protections
        user.refresh_from_db()
        assert user.first_name == "NewFirst"
        assert user.last_name == "NewLast"
        assert user.email != "hacker@example.com"
        assert user.role == "customer"
