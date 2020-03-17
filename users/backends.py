from typing import Optional

from django.contrib.auth.backends import ModelBackend

from users.helpers import verify_credo_user
from users.models import User


class CredoUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs) -> Optional[User]:
        ret = verify_credo_user(username, password)
        if ret:
            return User.get_or_create_from_credo(ret, ret.get('token'))
        return None
