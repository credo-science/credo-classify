import urllib.parse
from random import randrange
from typing import Optional

from django.db import models

from credo_classification.drf import DjangoPlusViewPermissionsMixin
from users.models import User


class Team(models.Model):
    """
    CREDO Team imported from original CREDO Database.

    The id and name fields are imported from team_mapping.json.
    """
    name = models.CharField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return "Team %s" % self.name

    class Meta(DjangoPlusViewPermissionsMixin):
        pass


class CredoUser(models.Model):
    """
    CREDO User imported from original CREDO Database.

    The id, username and display_name fields are imported from user_mapping.json.
    """
    username = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)

    def __str__(self):
        return "User %s (%d)" % (self.display_name, self.id)

    class Meta(DjangoPlusViewPermissionsMixin):
        pass


class Device(models.Model):
    """
    CREDO Device imported from original CREDO Database.

    The id, device_id, device_type, device_model, system_version and user fields are imported from device_mapping.json.
    """
    device_id = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255, default="phone_android")
    device_model = models.CharField(max_length=255)
    system_version = models.CharField(max_length=255)
    user = models.ForeignKey(CredoUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Device %s (%s)" % (self.device_id, self.device_model)

    class Meta(DjangoPlusViewPermissionsMixin):
        pass


class Detection(models.Model):
    """
    CREDO Detection imported from original CREDO Database.

    The id, device, user, team, timestamp, time_received and metadata fields are imported from detections/*.json.
    The frame_content was decoded and stored in file system.
    Reset attributes are stored in DetectionAttribute.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(CredoUser, on_delete=models.CASCADE, db_index=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_index=True)
    timestamp = models.BigIntegerField(db_index=True)
    time_received = models.BigIntegerField(blank=True)
    source = models.CharField(max_length=255, blank=True)
    provider = models.CharField(max_length=255, blank=True)
    metadata = models.TextField(null=True, blank=True)

    has_image = models.BooleanField(db_index=True)
    mime = models.CharField(max_length=32, blank=True, null=True)
    frame_content = models.BinaryField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    # helpers for randomize hits for classifiers
    random = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return "Detection %s" % self.id

    def get_file_name(self) -> Optional[str]:
        ext = 'dat'
        if self.mime == 'image/png':
            ext = 'png'

        return '%09d.%s' % (self.id, ext)

    def get_file_url(self) -> str:
        from credo_classification.settings import BASE_URL
        url = urllib.parse.urljoin('/' + BASE_URL, 'images/')
        url = urllib.parse.urljoin(url, self.get_file_name())
        return url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.random is None:
            self.random = randrange(-2147483648, 2147483647)
        super().save(force_insert, force_update, using, update_fields)

    class Meta(DjangoPlusViewPermissionsMixin):
        index_together = [
            ("has_image", "score", "random"),
            ("user", "has_image", "score", "random"),
            ("team", "has_image", "score", "random"),
        ]


class Ping(models.Model):
    """
    Ping's of detecion running imported from original CREDO Database.
    """
    timestamp = models.BigIntegerField(db_index=True)
    time_received = models.BigIntegerField(blank=True)
    delta_time = models.IntegerField(blank=True, null=True)
    on_time = models.IntegerField(blank=True, null=True, default=0)

    metadata = models.TextField(null=True, blank=True)

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(CredoUser, on_delete=models.CASCADE)

    def __str__(self):
        return "Ping %s" % self.id
