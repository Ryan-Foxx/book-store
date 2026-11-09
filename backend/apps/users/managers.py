from django.contrib.auth.models import BaseUserManager
from django.db import models

from .validators import normalize_ir_mobile


class UserQuerySet(models.QuerySet):
    """
    Custom QuerySet for User model.

    Certain fields in the User model have security, validation, and lifecycle implications.
    Direct updates via querysets bypass save() and model signals, leading to inconsistent
    database state or missed security events (e.g., token revocation).
    """

    # Fields that must never be updated in bulk via SQL bypassing save() / signals
    PROTECTED_BULK_UPDATE_FIELDS = {
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "password",
        "phone_number",
    }

    def update(self, **kwargs):
        """
        Prevent bypassing User.save(), full_clean(), and security signals
        during bulk SQL update operations.
        """
        unsafe_fields = set(kwargs.keys()) & self.PROTECTED_BULK_UPDATE_FIELDS

        if unsafe_fields:
            raise ValueError(
                "Bulk update of protected User fields is forbidden. "
                f"Use a service method or instance.save() instead: {sorted(unsafe_fields)}"
            )

        return super().update(**kwargs)

    def bulk_update(self, objs, fields, batch_size=None):
        """
        Prevent bypassing validation and security signals during bulk_update().
        """
        unsafe_fields = set(fields) & self.PROTECTED_BULK_UPDATE_FIELDS

        if unsafe_fields:
            raise ValueError(
                "Bulk update of protected User fields is forbidden. "
                f"Use a service method or instance.save() instead: {sorted(unsafe_fields)}"
            )

        return super().bulk_update(
            objs,
            fields,
            batch_size=batch_size,
        )

    def bulk_create(
        self,
        objs,
        batch_size=None,
        ignore_conflicts=False,
        update_conflicts=False,
        update_fields=None,
        unique_fields=None,
    ):
        """
        Prevent raw bulk insertion of User instances.

        Why:
        - Skips model save() and full_clean()
        - Bypasses post_save signals (e.g., UserProfile creation)
        - Bypasses password hashing and phone normalization
        """

        raise ValueError(
            "bulk_create() is not allowed for User model. "
            "Use User.objects.create_user() or create instances individually."
        )


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    """
    Custom manager for User model providing custom creation logic
    and hooking into the hardened UserQuerySet.
    """

    def create_user(
        self,
        username,
        email,
        phone_number,
        password=None,
        **extra_fields,
    ):
        """
        Create and persist a regular user with sanitized and normalized inputs.
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
        # save() executes full_clean() and role/permission synchronization
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        username,
        email,
        phone_number,
        password=None,
        **extra_fields,
    ):
        """
        Create and persist a superuser.

        Enforces 'owner' role and root permissions explicitly.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", self.model.ROLE_CHOICE_OWNER)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if extra_fields.get("role") != self.model.ROLE_CHOICE_OWNER:
            raise ValueError(f"Superuser must have role='{self.model.ROLE_CHOICE_OWNER}'.")

        return self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )
