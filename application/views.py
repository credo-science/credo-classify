from django.db.models import Model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from application.models import Team, CredoUser, Device
from application.serializers import TeamsFileSerializer, CredoUsersFileSerializer, DevicesFileSerializer


class GenericImporter(APIView):

    # need to set in inherit
    serializer_class = None  # JSON parser of whole JSON file
    unit_name = None  # field with array of imported data
    model_class = None
    fields_to_import = []  # field names list to be imported except 'id'

    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        parsed = 0
        inserted = 0
        updated = 0
        not_changed = 0

        for unit in serializer.validated_data.get(self.unit_name, []):
            parsed += 1
            v_id = unit.get('id')
            v_fields = {}
            for f in self.fields_to_import:
                v_fields[f] = unit.get(f)

            v = self.model_class.objects.filter(pk=v_id).first()  # type: Model
            if v is None:
                inserted += 1
                self.model_class.objects.create(id=v_id, **v_fields)
            else:
                changed = False
                for key, value in v_fields.items():
                    if getattr(v, key) != value:
                        changed = True
                        setattr(v, key, value)

                if changed:
                    updated += 1
                    v.save()
                else:
                    not_changed += 1

        return Response({
            'parsed': parsed,
            'inserted': inserted,
            'updated': updated,
            'not_changed': not_changed
        })


class ImportTeams(GenericImporter):
    serializer_class = TeamsFileSerializer
    unit_name = 'teams'
    model_class = Team
    fields_to_import = ['name']


class ImportCredoUsers(GenericImporter):
    serializer_class = CredoUsersFileSerializer
    unit_name = 'users'
    model_class = CredoUser
    fields_to_import = ['username', 'display_name']


class ImportDevices(GenericImporter):
    serializer_class = DevicesFileSerializer
    unit_name = 'devices'
    model_class = Device
    fields_to_import = ['user_id', 'device_type', 'device_model', 'system_version']
