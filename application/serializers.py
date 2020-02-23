from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField
from django.utils.translation import gettext_lazy as _

from application.models import Team, CredoUser, Device


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team


class TeamImporterSerializer(Serializer):
    id = IntegerField(label=_("Team ID"))
    name = CharField(label=_("Team name"), allow_blank=True)


class TeamsFileSerializer(Serializer):
    teams = TeamImporterSerializer(many=True)


class CredoUserSerializer(ModelSerializer):
    class Meta:
        model = CredoUser


class CredoUserImporterSerializer(Serializer):
    id = IntegerField(label=_("User ID"))
    username = CharField(label=_("User name"), allow_blank=True)
    display_name = CharField(label=_("Display name"), allow_blank=True)


class CredoUsersFileSerializer(Serializer):
    users = CredoUserImporterSerializer(many=True)


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device


class DeviceImporterSerializer(Serializer):
    id = IntegerField(label=_("Device ID"))
    user_id = IntegerField(label=_("User ID"))
    device_type = CharField(label=_("Device type"), allow_blank=True)
    device_model = CharField(label=_("Device model"), allow_blank=True)
    system_version = CharField(label=_("OS version"), allow_blank=True)


class DevicesFileSerializer(Serializer):
    devices = DeviceImporterSerializer(many=True)
