from apps.users.models import User
from django.core.exceptions import ValidationError
from django.db import transaction


def _ensure_active_owner_remains(user: User):
    """
    Guard rule: prevent actions that would leave the system without any active owner.
    """
    if user.role == User.ROLE_CHOICE_OWNER:
        active_owners_count = (
            User.objects.select_for_update()
            .filter(role=User.ROLE_CHOICE_OWNER, is_active=True)
            .exclude(pk=user.pk)
            .count()
        )
        if active_owners_count == 0:
            raise ValidationError("Action aborted: the last active owner cannot be modified or demoted.")


@transaction.atomic
def change_user_role(*, user_id: int, new_role: str) -> User:
    """
    Safely change user role with concurrency protection and last-owner safety checks.
    """
    user = User.objects.select_for_update().get(pk=user_id)

    if user.role != new_role:
        _ensure_active_owner_remains(user)

    user.role = new_role
    user.save(update_fields=["role"])  # Triggers save() hook which syncs is_staff/is_superuser
    return user


@transaction.atomic
def deactivate_user(*, user_id: int) -> User:
    """
    Safely deactivate a user with concurrency protection and last-owner safety checks.
    """
    user = User.objects.select_for_update().get(pk=user_id)

    _ensure_active_owner_remains(user)

    user.is_active = False
    user.save(update_fields=["is_active"])  # Triggers token revocation via post_save
    return user
