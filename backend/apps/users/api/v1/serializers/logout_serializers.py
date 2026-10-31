from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class LogoutSerializer(serializers.Serializer):
    """
    Serializer responsible for invalidating (blacklisting) a refresh token.

    The client must send the refresh token that should be invalidated.
    Once blacklisted, the token can no longer be used to obtain new
    access tokens via the refresh endpoint.

    Example request body:

    {
        "refresh": "your_refresh_token_here"
    }
    """

    refresh = serializers.CharField(write_only=True)

    def save(self, **kwargs):
        """
        Blacklist the provided refresh token.

        If the token is invalid, expired, or already blacklisted,
        the exception is ignored to keep the logout operation
        idempotent (safe to call multiple times).
        """
        try:
            RefreshToken(self.validated_data["refresh"]).blacklist()
        except TokenError:
            pass
