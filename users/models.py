import binascii
import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from credo_classification.drf import DjangoPlusViewPermissionsMixin


class User(AbstractUser):
    """
    Auth user with;

    scores - points gained for classification of cosmic-ray hits
    """
    score = models.IntegerField(default=0)

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
