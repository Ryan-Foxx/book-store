from apps.books.models import BookDetail
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=BookDetail)
def delete_old_image_on_change(sender, instance, **kwargs):
    """
    Delete previous image file when a new one is uploaded.
    """
    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if not old.image:
        return

    if old.image == instance.image:
        return

    storage = old.image.storage

    if storage.exists(old.image.name):
        storage.delete(old.image.name)


@receiver(post_delete, sender=BookDetail)
def delete_image_on_BookDetail_delete(sender, instance, **kwargs):
    """
    Delete image file from storage when a BookDetail is deleted.
    """
    if not instance.image:
        return

    storage = instance.image.storage

    if storage.exists(instance.image.name):
        storage.delete(instance.image.name)
