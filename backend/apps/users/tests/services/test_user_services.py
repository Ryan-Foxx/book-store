import pytest
from apps.users.models import User
from apps.users.services.user_services import change_user_role, deactivate_user
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestUserServiceLayer:

    def test_change_user_role_success(self, customer_user):
        # Verify changing role from customer to admin works successfully
        updated_user = change_user_role(user_id=customer_user.pk, new_role=User.ROLE_CHOICE_ADMIN)

        assert updated_user.pk == customer_user.pk
        assert updated_user.role == User.ROLE_CHOICE_ADMIN
        # Role change should automatically sync staff permissions
        assert updated_user.is_staff is True
        assert updated_user.is_superuser is False

    def test_deactivate_user_success(self, customer_user):
        # Verify deactivating a standard customer user works successfully
        assert customer_user.is_active is True

        deactivated_user = deactivate_user(user_id=customer_user.pk)

        assert deactivated_user.pk == customer_user.pk
        assert deactivated_user.is_active is False

    def test_cannot_demote_or_deactivate_the_last_active_owner(self, owner_user):
        # Ensure that trying to demote the sole active owner raises ValidationError
        with pytest.raises(ValidationError) as excinfo:
            change_user_role(user_id=owner_user.pk, new_role=User.ROLE_CHOICE_CUSTOMER)

        assert "the last active owner cannot be modified or demoted" in str(excinfo.value)

        # Ensure that trying to deactivate the sole active owner also raises ValidationError
        with pytest.raises(ValidationError) as excinfo:
            deactivate_user(user_id=owner_user.pk)

        assert "the last active owner cannot be modified or demoted" in str(excinfo.value)

    def test_can_modify_owner_if_multiple_active_owners_exist(self, owner_user, user_factory):
        # Create a second active owner so the system safety guard allows modification
        second_owner = user_factory(role=User.ROLE_CHOICE_OWNER)

        # Now demoting the first owner should succeed because second_owner remains active
        updated_user = change_user_role(user_id=owner_user.pk, new_role=User.ROLE_CHOICE_ADMIN)

        assert updated_user.role == User.ROLE_CHOICE_ADMIN
        assert updated_user.is_superuser is False
        assert updated_user.is_staff is True
