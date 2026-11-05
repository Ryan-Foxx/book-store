from apps.users.validators import normalize_ir_mobile, validate_iranian_mobile
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    phone_number = serializers.CharField(
        required=True,
        validators=[
            validate_iranian_mobile,
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with this phone number already exists.",
            ),
        ],
    )

    def validate_phone_number(self, value):
        """
        Normalize mobile number to E.164 before validation/persistence.
        """
        return normalize_ir_mobile(value)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "phone_number", "role")
        read_only_fields = fields


class CurrentUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "phone_number", "role")
        read_only_fields = fields
