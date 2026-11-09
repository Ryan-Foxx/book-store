import pytest
from apps.users.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError


@pytest.mark.django_db
class TestUserModel:

    def test_create_user_success(self, user_factory, user_password):
        user = user_factory(
            username="johndoe",
            email="JohnDoe@Example.COM",
            phone_number="09123456789",
            role=User.ROLE_CHOICE_CUSTOMER,
        )
        assert user.pk is not None
        assert user.username == "johndoe"
        # Verify email is normalized to lower case
        assert user.email == "johndoe@example.com"
        # Verify password is properly hashed
        assert user.check_password(user_password)
        # Customer role should not have staff or superuser permissions
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_user_str_representation(self, user_factory):
        user = user_factory(username="testuser", role=User.ROLE_CHOICE_CUSTOMER)
        assert str(user) == "testuser (customer)"

    def test_role_sync_owner_sets_superuser_and_staff(self, user_factory):
        owner = user_factory(role=User.ROLE_CHOICE_OWNER)
        assert owner.is_superuser is True
        assert owner.is_staff is True

    def test_role_sync_admin_sets_staff_only(self, user_factory):
        admin = user_factory(role=User.ROLE_CHOICE_ADMIN)
        assert admin.is_superuser is False
        assert admin.is_staff is True

    def test_role_sync_customer_revokes_staff_and_superuser(self, user_factory):
        customer = user_factory(role=User.ROLE_CHOICE_CUSTOMER)
        assert customer.is_superuser is False
        assert customer.is_staff is False

    def test_unique_email_constraint(self, user_factory):
        user_factory(email="duplicate@example.com")
        with pytest.raises((IntegrityError, ValidationError)):
            user_factory(email="duplicate@example.com")

    def test_unique_phone_number_constraint(self, user_factory):
        user_factory(phone_number="09121112233")
        with pytest.raises((IntegrityError, ValidationError)):
            user_factory(phone_number="09121112233")

    def test_invalid_iranian_phone_number_raises_validation_error(self, user_factory):
        # Invalid phone format must trigger ValidationError on full_clean
        with pytest.raises(ValidationError):
            user = User(
                username="invalidphone",
                email="invalid@example.com",
                phone_number="123456",
                role=User.ROLE_CHOICE_CUSTOMER,
            )
            user.save()

    def test_phone_number_normalization_on_save(self, user_factory):
        # Verify that phone numbers are normalized to E.164 or canonical local format
        user = user_factory(phone_number="09123456789")
        assert user.phone_number.startswith("0912") or user.phone_number.startswith("+98")

    def test_user_queryset_update_blocks_protected_fields(self, user_factory):
        user = user_factory(role=User.ROLE_CHOICE_CUSTOMER)
        # Attempting bulk update on protected fields must raise ValueError
        with pytest.raises(ValueError) as excinfo:
            User.objects.filter(pk=user.pk).update(role=User.ROLE_CHOICE_ADMIN)
        assert "Bulk update of protected User fields is forbidden" in str(excinfo.value)

    def test_user_queryset_bulk_create_is_forbidden(self):
        # Model-level defense: bulk_create must be prohibited to prevent bypassing signals and hashing
        with pytest.raises(ValueError) as excinfo:
            User.objects.bulk_create([User(username="user1", email="u1@test.com", phone_number="09120000001")])
        assert "bulk_create() is not allowed for User model" in str(excinfo.value)
