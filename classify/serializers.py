from typing import Any, List

from rest_framework.serializers import SerializerMethodField, Serializer, ModelSerializer, CharField, IntegerField, FloatField
from django.utils.translation import gettext_lazy as _

from database.models import Team, CredoUser, Device, Ping, Detection
from database.serializers import DeviceSerializer
from definitions.models import Attribute
from definitions.serializers import AttributeSerializer


class DetectionClassifySerializer(ModelSerializer):
    device = DeviceSerializer(read_only=True)
    # values = DetectionAttributeSerializer(many=True)
    image = SerializerMethodField(read_only=True)
    attributes = SerializerMethodField(read_only=True)

    def get_image(self, o: Detection) -> str:
        return o.get_file_url()

    def get_attributes(self, o: Detection) -> List[dict]:
        ret = []
        for a in Attribute.objects.filter(kind='c', active=True):
            ret.append(AttributeSerializer(a).data)
        return ret

    class Meta:
        model = Detection
        fields = '__all__'
