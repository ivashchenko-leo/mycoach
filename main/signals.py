import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import CoachPhoto


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # This code is triggered whenever a new user has been created and saved to the database
    if created:
        Token.objects.create(user=instance)


@receiver(post_delete, sender=CoachPhoto)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem when corresponding `CoachPhoto` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
