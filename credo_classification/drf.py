import sys
import traceback

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback


class DjangoPlusViewModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class DjangoPlusViewPermissionsMixin:
    default_permissions = ('view', 'add', 'change', 'delete')


def api_500_handler(exception, context):
    response = exception_handler(exception, context)
    set_rollback()
    if response:
        return response
    else:
        if isinstance(exception, ValidationError):
            return Response({
                'error': True,
                'error_content': exception.get_full_details(),
                'status_code': 400},
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )
        else:
            print('500 Error: ' + str(exception))
            print("\n".join(traceback.format_exception(None, exception, exception.__traceback__)), file=sys.stderr, flush=True)
            return Response({
                    'error': True,
                    'error_content': str(exception),
                    'status_code': 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json"
            )
