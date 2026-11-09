from apps.users.models import UserProfile
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "username", "first_name", "last_name", "role")
        read_only_fields = ("id", "email", "phone_number", "username", "role")


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "avatar")
        read_only_fields = ("id",)

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        if user_data:
            # Use partial=True if updating nested user data in either PUT or PATCH
            user_serializer = UserSerializer(
                instance.user,
                data=user_data,
                partial=True,
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        return super().update(instance, validated_data)
