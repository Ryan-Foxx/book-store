from apps.users.models import UserProfile
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

User = get_user_model()


def _blacklist_user_refresh_tokens(user_id: int):
    """
    Helper function executed post-commit to safely blacklist all outstanding refresh tokens.
    """

    tokens = OutstandingToken.objects.filter(
        user_id=user_id,
        blacklistedtoken__isnull=True,
    )

    BlacklistedToken.objects.bulk_create(
        [BlacklistedToken(token=token) for token in tokens],
        ignore_conflicts=True,
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw=False, **kwargs):
    if raw or not created:
        return

    # Use get_or_create to prevent race-condition duplicates
    UserProfile.objects.get_or_create(user=instance)


@receiver(pre_save, sender=User)
def detect_security_context_changes(sender, instance, raw=False, **kwargs):
    """
    Detect critical security field changes before saving.
    Actual revocation is deferred to post_save on_commit to prevent premature invalidation.
    """
    if raw or not instance.pk:
        instance._revoke_tokens_needed = False
        return

    try:
        old_user = sender.objects.only("role", "is_active", "password").get(pk=instance.pk)
    except sender.DoesNotExist:
        instance._revoke_tokens_needed = False
        return

    role_changed = old_user.role != instance.role
    deactivated = old_user.is_active and not instance.is_active
    password_changed = old_user.password != instance.password

    instance._revoke_tokens_needed = role_changed or deactivated or password_changed


@receiver(post_save, sender=User)
def revoke_tokens_on_security_change(sender, instance, created, raw=False, **kwargs):
    """
    Revoke all outstanding refresh tokens only after the transaction is successfully committed.
    """

    if raw or created:
        return

    if getattr(instance, "_revoke_tokens_needed", False):
        transaction.on_commit(lambda: _blacklist_user_refresh_tokens(instance.pk))
