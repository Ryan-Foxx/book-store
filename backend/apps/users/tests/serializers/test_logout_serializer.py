import pytest
from apps.users.api.v1.serializers.logout_serializers import LogoutSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestLogoutSerializer:

    def test_logout_serializer_successful(self, user_factory):
        # Generate valid refresh token for the user
        user = user_factory()
        refresh = RefreshToken.for_user(user)

        data = {"refresh": str(refresh)}
        request_mock = type("Request", (), {"user": user})()

        serializer = LogoutSerializer(data=data, context={"request": request_mock})
        assert serializer.is_valid(), serializer.errors

        # Blacklist the token by invoking save
        serializer.save()

        # Token should no longer be valid once blacklisted
        with pytest.raises(Exception):
            refresh.check_valid()

    def test_logout_serializer_invalid_refresh_token(self, user_factory):
        user = user_factory()
        request_mock = type("Request", (), {"user": user})()

        # Malformed or unparseable token string
        data = {"refresh": "invalid-token-string-xyz"}
        serializer = LogoutSerializer(data=data, context={"request": request_mock})

        assert not serializer.is_valid()
        assert "refresh" in serializer.errors

    def test_logout_serializer_token_ownership_mismatch(self, user_factory):
        # Create two distinct users
        user_one = user_factory(username="userone")
        user_two = user_factory(username="usertwo")

        # Generate refresh token belonging to user_one
        refresh = RefreshToken.for_user(user_one)

        # Send logout request authenticated as user_two
        request_mock = type("Request", (), {"user": user_two})()
        serializer = LogoutSerializer(
            data={"refresh": str(refresh)},
            context={"request": request_mock},
        )

        # Cross-user token revocation must be rejected with AuthenticationFailed
        with pytest.raises(AuthenticationFailed):
            serializer.is_valid(raise_exception=True)
