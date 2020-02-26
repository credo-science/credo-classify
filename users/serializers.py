from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from users.models import User


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Invalid login or password.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    email = serializers.EmailField(label=_("Email"))

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')

        u = User.objects.filter(username=username, email=email).first()
        if u is None:
            msg = _('Invalid login or e-mail.')
            raise serializers.ValidationError(msg)
        else:
            msg = _('Reset password is not supported yet')
            raise serializers.ValidationError(msg)

        return attrs


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
