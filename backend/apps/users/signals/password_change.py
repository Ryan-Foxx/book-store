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
