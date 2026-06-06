from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers.logout import LogoutSerializer


class CustomUserViewSet(UserViewSet):
    """
    Customized Djoser UserViewSet.

    Default user-management endpoints are disabled because this project
    does not expose user resources through the authentication API.

    User-related data will instead be handled by a dedicated profile API.

    This endpoint is only used for authentication-related operations
    such as registration and account management.
    """

    http_method_names = ["post", "head", "options"]

    def get_view_name(self):
        action = getattr(self, "action", None)

        if action == "list":
            return "User Registration"

        return super().get_view_name()


class LogoutView(GenericAPIView):
    """
    Endpoint used to log out a user by invalidating their refresh token.

    This only logs out the session associated with the provided
    refresh token (per-device logout).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        """
        Handle logout requests.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
