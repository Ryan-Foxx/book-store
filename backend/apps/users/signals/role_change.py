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
