from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutSerializer(serializers.Serializer):
    """
    Serializer responsible for validating token ownership and blacklisting
    the provided refresh token.
    """

    refresh = serializers.CharField(write_only=True)

    def validate(self, attrs):
        refresh_str = attrs.get("refresh")
        request = self.context.get("request")

        try:
            token = RefreshToken(refresh_str)
        except (TokenError, InvalidToken):
            raise ValidationError({"refresh": "The refresh token is invalid or expired."})

        # Ensure the token belongs to the requesting authenticated user
        user_id_claim = api_settings.USER_ID_CLAIM
        token_user_id = token.payload.get(user_id_claim)

        user_id_field = api_settings.USER_ID_FIELD
        request_user_id = getattr(request.user, user_id_field)

        if str(token_user_id) != str(request_user_id):
            raise AuthenticationFailed("This token does not belong to the authenticated user.")

        attrs["token_instance"] = token
        return attrs

    def save(self, **kwargs):
        token = self.validated_data["token_instance"]
        try:
            token.blacklist()
        except TokenError:
            # Token may have already been blacklisted; keep operation idempotent
            pass
