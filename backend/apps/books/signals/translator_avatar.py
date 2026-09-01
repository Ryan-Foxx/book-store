from apps.books.models import Translator
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Translator)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    """
    Delete previous avatar file when a new one is uploaded.
    """
    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if not old.avatar:
        return

    if old.avatar == instance.avatar:
        return

    storage = old.avatar.storage

    if storage.exists(old.avatar.name):
        storage.delete(old.avatar.name)


@receiver(post_delete, sender=Translator)
def delete_avatar_on_translator_delete(sender, instance, **kwargs):
    """
    Delete avatar file from storage when a Translator is deleted.
    """
    if not instance.avatar:
        return

    storage = instance.avatar.storage

    if storage.exists(instance.avatar.name):
        storage.delete(instance.avatar.name)
