from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField
from django.utils.translation import gettext_lazy as _

from application.models import Team


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team


class TeamImporterSerializer(Serializer):
    id = IntegerField(label=_("Team ID"))
    name = CharField(label=_("Team name"), allow_blank=True)


class TeamsFileSerializer(Serializer):
    teams = TeamImporterSerializer(many=True)
