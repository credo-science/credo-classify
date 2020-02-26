from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Token
from users.serializers import AuthTokenSerializer, UserViewSerializer


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
