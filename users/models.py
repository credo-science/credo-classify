from django.contrib.auth.models import AbstractUser
from django.db import models

from credo_classification.drf import DjangoPlusViewPermissionsMixin


class User(AbstractUser):
    """
    Auth user with;

    scores - points gained for classification of cosmic-ray hits
    """
    score = models.IntegerField(default=0)

    class Meta(DjangoPlusViewPermissionsMixin):
        pass
