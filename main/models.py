import uuid

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField

from django.utils.timezone import now


def upload_photo(photo, filename):
    return "images/%s/%s" % (photo.user.id, filename)


class Sport(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()

    def __str__(self):
        return self.name + " (" + str(self.code) + ")"

    class Meta:
        db_table = 'sports'


class CoachPhoto(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_photo)

    class Meta:
        db_table = 'coach_photos'


class CoachProfile(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    timestamp = models.DateTimeField(default=now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = JSONField()
    sports = models.ManyToManyField(Sport)
    photos = models.ManyToManyField(CoachPhoto)
    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = 'coach_profiles'


class CoachPost(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    title = models.TextField()
    content = JSONField()
    is_public = models.BooleanField(default=False)
    tags = models.TextField()

    class Meta:
        db_table = 'coach_posts'
