import os
import uuid

from apps.users.models import UserProfile
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=UserProfile)
def rename_user_profile_avatar(sender, instance, created, **kwargs):
    """
    Rename avatar file after upload from temporary name to UUID filename.

    Workflow:
    temp_<filename>  →  <uuid>.<ext>

    Uses Django storage API so it works with:
    - local filesystem
    - S3
    - any custom storage backend
    """

    if not instance.avatar:
        return

    old_name = instance.avatar.name

    if not old_name.startswith("users/user-profiles/avatars/temp_"):
        return

    storage = instance.avatar.storage

    ext = os.path.splitext(old_name)[1]
    new_filename = f"{uuid.uuid4().hex}{ext}"

    new_path = f"users/user-profiles/avatars/{new_filename}"

    if storage.exists(old_name):

        with storage.open(old_name, "rb") as old_file:
            storage.save(new_path, old_file)

        storage.delete(old_name)

        sender.objects.filter(pk=instance.pk).update(avatar=new_path)


@receiver(pre_save, sender=UserProfile)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    """
    Delete previous avatar file when a new one is uploaded.
    Uses Django storage API so it works with any storage backend.
    """

    if not instance.pk:
        return

    try:
        old_profile = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_avatar = old_profile.avatar
    new_avatar = instance.avatar

    if not old_avatar:
        return

    if old_avatar == new_avatar:
        return

    storage = old_avatar.storage

    if storage.exists(old_avatar.name):
        storage.delete(old_avatar.name)


@receiver(post_delete, sender=UserProfile)
def delete_avatar_on_profile_delete(sender, instance, **kwargs):
    """
    Delete avatar file from storage when a UserProfile is deleted.
    Works with any Django storage backend.
    """

    if not instance.avatar:
        return

    avatar = instance.avatar
    storage = avatar.storage

    if storage.exists(avatar.name):
        storage.delete(avatar.name)
