from django.contrib.auth.models import AbstractUser
from django.db import models
from seval import safe_eval  # type: ignore

from credo_classification.drf import DjangoPlusViewPermissionsMixin


class User(AbstractUser):
    """
    Auth user with;

    scores - points gained for classification of cosmic-ray hits
    """
    score = models.IntegerField(default=0)

    class Meta(DjangoPlusViewPermissionsMixin):
        pass


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


class Attribute(models.Model):
    """
    Attribute definition for cosmic-ray hits. It is simple RDF based semantic net attribute.

    All attributes store float64 value (15+ significant digits).
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return 'Attribute: %s' % self.name

    class Meta(DjangoPlusViewPermissionsMixin):
        unique_together = [['name']]


class Relation(models.Model):
    """
    Semantic net relation between attributes.

    Weight of relation is evaluated by arithmetic function executed by seval library. I.e.:
    evaluation='x * 2', where x was replaced by src attribute value
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    src = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='relation_src')
    dest = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='relation_dest')
    evaluation = models.CharField(max_length=255, default='x')

    def evaluate_weight(self, src_value: float) -> float:
        """
        Evaluate weight of relation.

        :param src_value: float-value of source attribute
        :return: evaluated weight of relation
        """
        return float(safe_eval(self.evaluation.replace('x', str(src_value))))

    def __str__(self) -> str:
        return 'Attribute: %s' % self.name

    class Meta(DjangoPlusViewPermissionsMixin):
        unique_together = [['src', 'dest']]


class Detection(models.Model):
    """
    CREDO Detection imported from original CREDO Database.

    The id, device, user, team, timestamp, time_received and metadata fields are imported from detections/*.json.
    The frame_content was decoded and stored in file system.
    Reset attributes are stored in DetectionAttribute.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    timestamp = models.BigIntegerField(db_index=True)
    time_received = models.BigIntegerField(blank=True)
    mime = models.CharField(max_length=32, default='image/png')
    source = models.CharField(max_length=255, blank=True)
    provider = models.CharField(max_length=255, blank=True)
    metadata = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Detection %s" % self.id

    def get_filename(self):
        """
        File name where frame_content was stored.
        :return: absolute path for file with decoded data
        """
        from credo_classification.settings import FILES_STORAGE
        import os

        ext = 'dat'
        if self.mime == 'image/png':
            ext = 'png'

        return os.path.join(FILES_STORAGE, '%d.%s' % (self.id, ext))

    class Meta(DjangoPlusViewPermissionsMixin):
        pass


class DetectionAttribute(models.Model):
    """
    Attribute of cosmic-ray hit. Attribute was provided by various author and can be different by each author.
    """
    detection = models.ForeignKey(Detection, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    value = models.FloatField()

    class Meta(DjangoPlusViewPermissionsMixin):
        unique_together = [['detection', 'attribute', 'author']]


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Ping %s" % self.id
