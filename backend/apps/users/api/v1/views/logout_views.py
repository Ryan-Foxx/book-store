from apps.users.api.v1.serializers.logout_serializers import LogoutSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class LogoutView(GenericAPIView):
    """
    Endpoint used to log out a user by blacklisting their refresh token.
    Per-device logout; only invalidates the session tied to the sent refresh token.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        # Pass request context so the serializer can verify token ownership
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_205_RESET_CONTENT,
        )
