from apps.users.models import UserProfile
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "username", "first_name", "last_name", "role")
        read_only_fields = ("id", "email", "phone_number", "role")


class UserProfileSerializer(serializers.ModelSerializer):

    # Nested Serializer Fields
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ("id", "user", "avatar")
        read_only_fields = ("id",)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=self.partial)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        return super().update(instance, validated_data)
