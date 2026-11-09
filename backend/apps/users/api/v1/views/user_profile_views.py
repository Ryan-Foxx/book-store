from apps.users.api.v1.serializers.user_profile_serializers import UserProfileSerializer
from apps.users.models import UserProfile
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            raise NotFound("Profile not found for this user.")
