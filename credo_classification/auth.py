from typing import Type

from django.db.models.base import Model
from rest_framework.authentication import TokenAuthentication


class MyTokenAuthentication(TokenAuthentication):

    def get_model(self) -> Type[Model]:
        from users.models import Token
        return Token
