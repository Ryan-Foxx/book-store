from django.contrib.auth.models import BaseUserManager

from .validators import normalize_ir_mobile


class UserManager(BaseUserManager):
    """
    Custom manager for User model.

    Ensures consistent user creation across the project and enforces
    required fields and normalization rules.
    """

    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        """
        Create and return a regular user.

        Enforces:
        - email normalization
        - phone number normalization
        - password hashing
        """

        if not username:
            raise ValueError("The username must be set.")

        if not email:
            raise ValueError("The email address must be set.")

        if not phone_number:
            raise ValueError("The phone number must be set.")

        email = self.normalize_email(email)
        phone_number = normalize_ir_mobile(phone_number)

        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        """
        Create and return a superuser.

        Superusers are always assigned the 'owner' role.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "owner")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )
