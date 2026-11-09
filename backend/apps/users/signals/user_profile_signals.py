from apps.users.models import UserProfile
from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=UserProfile)
def stage_old_avatar_for_deletion(sender, instance, raw=False, **kwargs):
    """
    Identify and stage the old avatar file path if it is being replaced or removed.
    """

    if raw or not instance.pk:
        return

    try:
        old_profile = sender.objects.only("avatar").get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_avatar = old_profile.avatar
    # If old avatar exists and is different from the incoming one, stage for deletion
    if old_avatar and old_avatar != instance.avatar:
        instance._old_avatar_name = old_avatar.name
        instance._avatar_storage = old_avatar.storage


@receiver(post_save, sender=UserProfile)
def cleanup_old_avatar_on_commit(sender, instance, raw=False, **kwargs):
    """
    Delete the replaced avatar file from storage only after the DB transaction succeeds.
    """
    if raw:
        return

    old_avatar_name = getattr(instance, "_old_avatar_name", None)
    storage = getattr(instance, "_avatar_storage", None)

    if old_avatar_name and storage:
        transaction.on_commit(lambda: storage.delete(old_avatar_name) if storage.exists(old_avatar_name) else None)


@receiver(post_delete, sender=UserProfile)
def delete_avatar_on_profile_delete(sender, instance, raw=False, **kwargs):
    """
    Delete avatar file from storage when a UserProfile is deleted, deferred to on_commit.
    """

    if raw or not instance.avatar:
        return

    storage = instance.avatar.storage
    avatar_name = instance.avatar.name

    transaction.on_commit(lambda: storage.delete(avatar_name) if storage.exists(avatar_name) else None)
