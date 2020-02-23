from django.db import models

from credo_classification.drf import DjangoPlusViewPermissionsMixin
from database.models import Detection
from definitions.models import Attribute
from users.models import User


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
