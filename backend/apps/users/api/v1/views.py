from apps.users.models import UserProfile
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers.logout import LogoutSerializer
from .serializers.user_profile import UserProfileSerializer
from .throttles import (
    ActivationRateThrottle,
    LoginRateThrottle,
    RegisterRateThrottle,
    ResendActivationRateThrottle,
    ResetPasswordConfirmRateThrottle,
    ResetPasswordRateThrottle,
    ResetUsernameRateThrottle,
    SetPasswordRateThrottle,
    SetUsernameRateThrottle,
)


class UserProfileViewSet(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            raise NotFound("Profile not found for this user.")


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

    def get_throttles(self):
        if self.action == "create":
            self.throttle_classes = [RegisterRateThrottle]

        elif self.action == "activation":
            self.throttle_classes = [ActivationRateThrottle]

        elif self.action == "resend_activation":
            self.throttle_classes = [ResendActivationRateThrottle]

        elif self.action == "reset_password":
            self.throttle_classes = [ResetPasswordRateThrottle]

        elif self.action == "reset_username":
            self.throttle_classes = [ResetUsernameRateThrottle]

        elif self.action == "reset_password_confirm":
            self.throttle_classes = [ResetPasswordConfirmRateThrottle]

        elif self.action == "set_password":
            self.throttle_classes = [SetPasswordRateThrottle]

        elif self.action == "set_username":
            self.throttle_classes = [SetUsernameRateThrottle]

        return super().get_throttles()

    def get_view_name(self):
        action = getattr(self, "action", None)

        if action == "list":
            return "User Registration"

        return super().get_view_name()


class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]


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
