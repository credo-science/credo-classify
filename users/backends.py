from typing import Optional

from django.contrib.auth.backends import ModelBackend

from users.helpers import verify_credo_user
from users.models import User


class CredoUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs) -> Optional[User]:
        ret = verify_credo_user(username, password)
        if ret:
            user = User.objects.filter(username=username).first()
            if user is None:
                user = User.objects.create(
                    username=username,
                    email=ret.get('email')
                )
            return user
        return None
