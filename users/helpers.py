from typing import Optional

from django.conf import settings
from requests import Response, post


def gen_api_request():
  return {
    "device_id": settings.APP_SITE,
    "device_type": settings.APP_NAME,
    "device_model": settings.APP_NAME,
    "system_version": settings.APP_VERSION,
    "app_version": settings.APP_VERSION
  }


def verify_credo_user(username: str, password: str) -> Optional[dict]:

  data = {
    "username": username,
    "password": password,
    **gen_api_request()
  }

  ret = post('%sapi/v2/user/login' % settings.CREDO_SERVER, json=data)  # type: Response
  if ret.status_code == 400:
    return None
  return ret.json()


def verify_user_by_credo_token(credo_token: str) -> Optional[dict]:
  headers = {"Authorization": "Token %s" % credo_token}
  ret = post('%sapi/v2/user/info' % settings.CREDO_SERVER, json=gen_api_request(), headers=headers)
  if ret.status_code == 200:
    return ret.json()
  return None
