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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def revoke_tokens_on_role_change(sender, instance, **kwargs):
    """

    Security signal: revoke all JWT refresh tokens when a user’s role changes.

    In this project, the role field is the single source of truth for

    authorization and directly controls is_staff and is_superuser.

    When a role changes, the user’s security context changes as well

    (e.g., admin → customer or customer → admin). Existing authentication

    sessions may therefore carry outdated privilege assumptions.

    To ensure consistent authorization behavior, all outstanding refresh

    tokens are revoked whenever the role changes. Users must authenticate

    again to obtain tokens reflecting their new permissions.
    """
    if not instance.pk:
        return

    try:
        old_user = User.objects.only("role").get(pk=instance.pk)
    except User.DoesNotExist:
        return

    if old_user.role == instance.role:
        return

    with transaction.atomic():
        tokens = OutstandingToken.objects.filter(
            user=instance,
            blacklistedtoken__isnull=True,
        )

        BlacklistedToken.objects.bulk_create([BlacklistedToken(token=token) for token in tokens])


@receiver(pre_save, sender=User)
def revoke_tokens_on_user_deactivation(sender, instance, **kwargs):
    """

    Security signal: revoke all JWT refresh tokens when a user account is deactivated.

    If a user account becomes inactive (is_active=False), all existing authentication

    sessions must immediately become invalid. Without explicit revocation, previously

    issued refresh tokens could still be used to obtain new access tokens until they

    expire.

    This signal listens for changes to the is_active field and blacklists all

    outstanding (non‑blacklisted) refresh tokens when the account is deactivated.

    Typical scenarios include:

    administrative account suspension
    security lockdown after suspicious activity
    compliance or moderation actions
    By revoking all refresh tokens, the system guarantees that the user cannot

    continue using any previously authenticated sessions.
    """
    if not instance.pk:
        return

    try:
        old_user = User.objects.only("is_active").get(pk=instance.pk)
    except User.DoesNotExist:
        return

    # Only trigger when the account transitions from active → inactive
    if old_user.is_active and not instance.is_active:

        with transaction.atomic():
            tokens = OutstandingToken.objects.filter(
                user=instance,
                blacklistedtoken__isnull=True,
            )

            BlacklistedToken.objects.bulk_create([BlacklistedToken(token=token) for token in tokens])


@receiver(pre_save, sender=User)
def revoke_tokens_on_password_change(sender, instance, **kwargs):
    """

    Security signal: revoke all JWT refresh tokens when a user’s password changes.

    JWTs are stateless by nature, meaning previously issued tokens remain valid

    until they expire. If a password changes, any existing refresh tokens could

    still be used to obtain new access tokens unless they are explicitly revoked.

    This signal listens for password changes and blacklists all outstanding

    (non‑blacklisted) refresh tokens belonging to the user. This forces all

    existing sessions on all devices to re-authenticate.

    The signal works regardless of how the password was changed:

    Django admin
    password reset flow
    API password change
    custom business logic
    """

    if not instance.pk:
        return

    try:
        old_user = User.objects.only("password").get(pk=instance.pk)
    except User.DoesNotExist:
        return

    if old_user.password == instance.password:
        return

    with transaction.atomic():
        tokens = OutstandingToken.objects.filter(
            user=instance,
            blacklistedtoken__isnull=True,
        )

        BlacklistedToken.objects.bulk_create([BlacklistedToken(token=token) for token in tokens])
