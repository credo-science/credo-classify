from django.db import models
from django.utils.translation import gettext_lazy as _

from credo_classification.drf import DjangoPlusViewPermissionsMixin
from database.models import Detection
from users.models import User


class Classified(models.Model):
    """
    Classify register table.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    detection = models.ForeignKey(Detection, on_delete=models.CASCADE, verbose_name=_('Detection'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of classified'))

    class Meta(DjangoPlusViewPermissionsMixin):
        verbose_name = _('Classified detection')
        verbose_name_plural = _('Classified detections')
        unique_together = [['user', 'detection']]
