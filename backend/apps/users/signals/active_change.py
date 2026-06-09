from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

User = get_user_model()


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
