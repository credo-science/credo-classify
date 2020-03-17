from django.conf import settings
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from users.helpers import verify_user_by_credo_token
from users.models import Token, User
from users.serializers import AuthTokenSerializer, UserViewSerializer, ResetPasswordSerializer


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': UserViewSerializer(user).data})


obtain_auth_token = ObtainAuthToken.as_view()


def auth_by_detector(request):
    credo_token = request.GET.get('token')
    message = ''
    token = ''
    user_json = {}
    try:
        json = verify_user_by_credo_token(credo_token)
        if json is None:
            message = _('Invalid CREDO token')
        else:
            user = User.get_or_create_from_credo(json, credo_token)
            token = Token.objects.create(user=user).key
            user_json = UserViewSerializer(user).data
    except:
        message = _('Connection error with CREDO database')

    context = {
        'token': token,
        'message': message,
        'user': user_json,
        'base_url': settings.BASE_URL
    }
    return render(request, 'auth.html', context)


class VoidToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({})


void_token = VoidToken.as_view()


class ResetPassword(APIView):
    permission_classes = ()
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: implement
        return Response({})


reset_password = ResetPassword.as_view()