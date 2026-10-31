from apps.users.api.v1.serializers.logout_serializers import LogoutSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
