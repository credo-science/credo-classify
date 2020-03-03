from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField, FloatField
from django.utils.translation import gettext_lazy as _

from database.models import Team, CredoUser, Device, Ping, Detection


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
        fields = '__all__'


class DeviceImporterSerializer(Serializer):
    id = IntegerField(label=_("Device ID"))
    user_id = IntegerField(label=_("User ID"))
    device_type = CharField(label=_("Device type"), allow_blank=True)
    device_model = CharField(label=_("Device model"), allow_blank=True)
    system_version = CharField(label=_("OS version"), allow_blank=True)


class DevicesFileSerializer(Serializer):
    devices = DeviceImporterSerializer(many=True)


class PingSerializer(ModelSerializer):
    class Meta:
        model = Ping


class PingImporterSerializer(Serializer):
    id = IntegerField(label=_("Ping ID"))
    user_id = IntegerField(label=_("User ID"))
    device_id = IntegerField(label=_("Device ID"))
    timestamp = IntegerField(label=_("Timestamp"))
    time_received = IntegerField(label=_("Time received"))
    delta_time = IntegerField(label=_("Delta time"), allow_null=True)
    on_time = IntegerField(label=_("On time"))
    metadata = CharField(label=_("Metadata"), allow_blank=True, allow_null=True)


class PingFileSerializer(Serializer):
    pings = PingImporterSerializer(many=True)


class DetectionSerializer(ModelSerializer):
    class Meta:
        model = Detection


class DetectionImporterSerializer(Serializer):
    id = IntegerField(label=_("Detection ID"))
    user_id = IntegerField(label=_("User ID"))
    device_id = IntegerField(label=_("Device ID"))
    team_id = IntegerField(label=_("Team ID"))
    timestamp = IntegerField(label=_("Timestamp"))
    time_received = IntegerField(label=_("Time received"))
    source = CharField(label=_("Source"))
    provider = CharField(label=_("Provider"))
    metadata = CharField(label=_("Metadata"), allow_blank=True, allow_null=True)

    # stored in DetectionAttribute
    accuracy = FloatField(label=_("Team ID"))
    latitude = FloatField(label=_("Team ID"))
    longitude = FloatField(label=_("Team ID"))
    altitude = FloatField(label=_("Team ID"))
    height = IntegerField(label=_("Team ID"))
    width = IntegerField(label=_("Team ID"))
    x = IntegerField(label=_("Team ID"), allow_null=True)
    y = IntegerField(label=_("Team ID"), allow_null=True)

    # stored in file system
    frame_content = CharField(label=_("Metadata"), allow_blank=True, allow_null=True)


class DetectionFileSerializer(Serializer):
    detections = DetectionImporterSerializer(many=True)
