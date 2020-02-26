from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from users.models import Token
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