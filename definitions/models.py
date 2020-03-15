from django.db import models
from seval import safe_eval
from django.utils.translation import gettext_lazy as _

from credo_classification.drf import DjangoPlusViewPermissionsMixin
from users.models import User


class Attribute(models.Model):
    """
    Attribute definition for cosmic-ray hits. It is simple RDF based semantic net attribute.

    All attributes store float64 value (15+ significant digits).
    """
    KIND_CHOICES = (
        ('b', _('Build-in')),
        ('c', _('Classification by user')),
        ('cs', _('Scaled classification (1 to 5)')),
        ('co', _('One class')),
        ('o', _('Others')),
    )

    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    description = models.TextField(default='', blank=True, verbose_name=_('Description'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Author'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))
    kind = models.CharField(max_length=2, default='o', choices=KIND_CHOICES, verbose_name=_('Kind'))

    def __str__(self) -> str:
        return _('Attribute: %s') % self.name

    class Meta(DjangoPlusViewPermissionsMixin):
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')
        ordering = ['name']


class Relation(models.Model):
    """
    Semantic net relation between attributes.

    Weight of relation is evaluated by arithmetic function executed by seval library. I.e.:
    evaluation='x * 2', where x was replaced by src attribute value
    """
    name = models.CharField(max_length=255)
    description = models.TextField(default='', blank=True)
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
