from rest_framework.serializers import ModelSerializer, Serializer, ModelSerializer, CharField, IntegerField, FloatField
from django.utils.translation import gettext_lazy as _

from database.models import Team, CredoUser, Device, Ping, Detection
from database.serializers import DeviceSerializer
from values.models import DetectionAttribute


class DetectionAttributeSerializer(ModelSerializer):

    class Meta:
        model = DetectionAttribute
