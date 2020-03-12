from typing import Optional

from django.conf import settings
from requests import Response, post


def verify_credo_user(username: str, password: str) -> Optional[dict]:

  data = {
    "username": username,
    "password": password,
    "device_id": settings.APP_SITE,
    "device_type": settings.APP_NAME,
    "device_model": settings.APP_NAME,
    "system_version": settings.APP_VERSION,
    "app_version": settings.APP_VERSION
  }

  ret = post('%sapi/v2/user/login' % settings.CREDO_SERVER, json=data)  # type: Response
  if ret.status_code == 400:
    return None
  return ret.json()
