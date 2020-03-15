from typing import Tuple

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

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
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of classified'))

    @staticmethod
    def set_or_update_value(detection_id: int, user: User, attribute: str, value: float) -> Tuple['DetectionAttribute', bool]:
        """
        Store or update attribute value
        :param detection_id: ID of detection hit
        :param user: author of value
        :param attribute: name of attribute
        :param value: value of attribute
        :return: tuple with created entity and True or False when created or updated
        """
        created = True
        a = DetectionAttribute.objects.filter(
            detection_id=detection_id, author=user, attribute__name=attribute
        ).first()  # type: DetectionAttribute
        if a is None:
            a = DetectionAttribute.objects.create(
                detection_id=detection_id, author=user, attribute=Attribute.objects.get(name=attribute), value=value
            )
        else:
            a.value = value
            a.date = now()
            a.save()
            created = False
        return a, created

    class Meta(DjangoPlusViewPermissionsMixin):
        unique_together = [['detection', 'attribute', 'author']]
