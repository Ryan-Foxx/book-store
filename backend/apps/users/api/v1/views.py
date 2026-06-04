from djoser.views import UserViewSet
from rest_framework.exceptions import NotFound


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
