from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager
from .validators import normalize_ir_mobile, validate_iranian_mobile


class User(AbstractUser):
    ROLE_CHOICE_OWNER = "owner"
    ROLE_CHOICE_ADMIN = "admin"
    ROLE_CHOICE_CUSTOMER = "customer"

    ROLE_CHOICES = [
        (ROLE_CHOICE_OWNER, "Owner"),
        (ROLE_CHOICE_ADMIN, "Admin"),
        (ROLE_CHOICE_CUSTOMER, "Customer"),
    ]

    email = models.EmailField(max_length=254, verbose_name="email address", unique=True)
    phone_number = models.CharField(max_length=15, unique=True, validators=[validate_iranian_mobile])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CHOICE_CUSTOMER)

    # Authentication still uses the username field
    USERNAME_FIELD = "username"

    # Required fields when creating a superuser via createsuperuser
    REQUIRED_FIELDS = ["email", "phone_number"]

    def clean(self):
        super().clean()

        # Normalize phone number before validation/storage
        if self.phone_number:
            self.phone_number = normalize_ir_mobile(self.phone_number)

        # Ensure permission flags stay consistent with the role
        self._sync_role_permissions()

    def _sync_role_permissions(self):
        """
        Synchronize role with is_staff and is_superuser.

        In this model, `role` is the single source of truth.
        Permission flags are always derived from the role to avoid
        inconsistent states.

        Rules:
        - owner    -> is_superuser=True,  is_staff=True
        - admin    -> is_superuser=False, is_staff=True
        - customer -> is_superuser=False, is_staff=False
        """

        if self.role == self.ROLE_CHOICE_OWNER:
            self.is_superuser = True
            self.is_staff = True

        elif self.role == self.ROLE_CHOICE_ADMIN:
            self.is_superuser = False
            self.is_staff = True

        else:  # customer
            self.is_superuser = False
            self.is_staff = False

    def save(self, *args, **kwargs):
        """
        Ensure model validation and role-permission synchronization
        are always applied before saving.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
