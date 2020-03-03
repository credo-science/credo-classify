from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _

from definitions.models import Attribute


class AttributeSerializer(ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'
