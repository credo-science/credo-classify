import binascii
import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _

from credo_classification.drf import DjangoPlusViewPermissionsMixin


class User(AbstractUser):
    """
    Auth user with;

    scores - points gained for classification of cosmic-ray hits (sum of all scores from Score table)
    verified - sum of verified scores from Score table
    """
    score = models.FloatField(default=0)
    verified = models.FloatField(default=0)

    @staticmethod
    def get_or_create_from_credo(credo: dict) -> 'User':
        username = credo.get('username')
        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.create(
                username=username,
                email=credo.get('email'),
                is_active=True
            )
        return user

    def update_scores(self) -> None:
        """
        Recalc scores from Score table and save.
        """
        from classify.models import DetectionScore
        self.score = DetectionScore.objects.filter(user=self).aggregate(score=Sum('score')).get('score', 0)
        self.verified = DetectionScore.objects.filter(user=self, verified=True).aggregate(verified=Sum('score')).get('verified', 0)
        self.save()

    def fast_update_scores(self, s: float, v: float) -> None:
        self.score += s
        self.verified += v
        User.objects.filter(username=self.username).update(score=F('score') + s)
        User.objects.filter(username=self.username).update(score=F('verified') + v)

    class Meta(DjangoPlusViewPermissionsMixin):
        pass


class Token(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    @staticmethod
    def void_all_tokens(user: User):
        Token.objects.filter(user=user).delete()

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
