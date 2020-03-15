from typing import Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _

from credo_classification.drf import DjangoPlusViewPermissionsMixin
from database.models import Detection
from definitions.models import Attribute
from users.models import User


class DetectionScore(models.Model):
    """
    Register scores and verification of honesty classify.

    scores - points gained for classification of cosmic-ray hits
    verified - scores are verified
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    detection = models.ForeignKey(Detection, on_delete=models.CASCADE, verbose_name=_('Detection'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of classified'))
    kind = models.CharField(max_length=2, choices=Attribute.KIND_CHOICES)

    score = models.FloatField(default=1)
    verified = models.BooleanField(default=False)

    @staticmethod
    def set_new_points(user: User, detection: Detection, kind: str, score: int = 1) -> Tuple[float, float]:
        """
        Create or update score for classify.
        :param user: author of classify
        :param detection: classified hit
        :param kind: kind of classification, @see Attribute.kind
        :param score: unverified scores for classify hit
        :return: tuple: s, v where s - all scores diff, v - verified scores diff
        """
        c = DetectionScore.objects.filter(user=user, detection=detection, kind=kind).first()
        v = score
        s = score
        if c is not None:
            if c.verified:
                v -= c.score
            s -= c.score
            c.delete()
        DetectionScore.objects.create(user=user, detection=detection, kind=kind, score=score)
        return s, v

    @staticmethod
    def has(user: User, detection: Detection, kind: str) -> bool:
        """

        :param user: author of classify
        :param detection: classified hit
        :param kind: kind of classification, @see Attribute.kind
        :return:
        """
        return DetectionScore.objects.filter(user=user, detection=detection, kind=kind).count() > 0

    class Meta(DjangoPlusViewPermissionsMixin):
        verbose_name = _('Classified detection')
        verbose_name_plural = _('Classified detections')
        unique_together = [['user', 'detection', 'kind']]
