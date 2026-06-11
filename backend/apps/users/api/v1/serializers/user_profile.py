from apps.users.models import UserProfile
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "username", "first_name", "last_name", "role")


class UserProfileSerializer(serializers.ModelSerializer):

    # Nested Serializer Fields
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "avatar")
        read_only_fields = ("id",)
