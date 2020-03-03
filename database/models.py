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
    user = models.ForeignKey(CredoUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    timestamp = models.BigIntegerField(db_index=True)
    time_received = models.BigIntegerField(blank=True)
    mime = models.CharField(max_length=32, default='image/png')
    source = models.CharField(max_length=255, blank=True)
    provider = models.CharField(max_length=255, blank=True)
    metadata = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Detection %s" % self.id

    def get_filepath(self) -> str:
        """
        Directory where file with frame_content was stored.
        :return: absolute path for directory
        """
        from credo_classification.settings import MEDIA_ROOT
        import os

        top = '%04d' % int(self.id / 100000000)
        middle = '%04d' % int(self.id / 10000)

        return os.path.join(MEDIA_ROOT, top, middle)

    def get_filename(self) -> str:
        """
        File name where frame_content was stored.
        :return: absolute path for file with decoded data
        """
        import os

        ext = 'dat'
        if self.mime == 'image/png':
            ext = 'png'

        return os.path.join(self.get_filepath(), '%09d.%s' % (self.id, ext))

    class Meta(DjangoPlusViewPermissionsMixin):
        pass


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
