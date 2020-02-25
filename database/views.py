import base64
import os
from typing import Any, Optional

from django.db.models import Model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from database.models import Team, CredoUser, Device, Ping, Detection
from database.serializers import TeamsFileSerializer, CredoUsersFileSerializer, DevicesFileSerializer, PingFileSerializer, DetectionFileSerializer
from definitions.models import Attribute
from values.models import DetectionAttribute


def default_to(v: Any, d: Any) -> Any:
    if v is None:
        return d
    return v


class GenericImporter(APIView):

    # need to set in inherit
    serializer_class = None  # JSON parser of whole JSON file
    unit_name = None  # field with array of imported data
    model_class = None
    fields_to_import = []  # field names list to be imported except 'id'

    permission_classes = [permissions.IsAdminUser]

    def nocheck_exists(self, request) -> bool:
        return bool(request.query_params.get('nocheck'))

    def post(self, request, *args, **kwargs):
        """
        Import fields_to_import values parsed by serializer_class from unit_name array to model_class model.

        Performance optimizations:
        - bulk insertion for new rows
        - if /?nocheck=1 then no checked existing row
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        parsed = 0
        inserted = 0
        updated = 0
        not_changed = 0

        check = not self.nocheck_exists(request)
        bulk = []

        for unit in serializer.validated_data.get(self.unit_name, []):
            parsed += 1
            v_id = unit.get('id')
            v_fields = {}
            for f in self.fields_to_import:
                v_fields[f] = unit.get(f)

            v = self.model_class.objects.filter(pk=v_id).first() if check else None  # type: Optional[Model]
            if v is None:
                inserted += 1
                e = self.model_class(id=v_id, **v_fields)
                bulk.append(e)
                self.import_as_attributes(e, unit, check)
            else:
                changed = False
                for key, value in v_fields.items():
                    if getattr(v, key) != value:
                        changed = True
                        setattr(v, key, value)

                attr_changed = self.import_as_attributes(v, unit, check)

                if changed:
                    v.save()
                if attr_changed or changed:
                    updated += 1
                else:
                    not_changed += 1

        if len(bulk):
            self.model_class.objects.bulk_create(bulk)

        self.bulk_attributes()

        return Response({
            'parsed': parsed,
            'inserted': inserted,
            'updated': updated,
            'not_changed': not_changed
        })

    def import_as_attributes(self, entity: Model, unit: dict, check: bool) -> bool:
        return False

    def bulk_attributes(self):
        pass


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


class ImportPings(GenericImporter):
    serializer_class = PingFileSerializer
    unit_name = 'pings'
    model_class = Ping
    fields_to_import = ['timestamp', 'time_received', 'delta_time', 'on_time', 'device_id', 'user_id', 'metadata']


class ImportDetections(GenericImporter):
    serializer_class = DetectionFileSerializer
    unit_name = 'detections'
    model_class = Detection
    fields_to_import = ['timestamp', 'time_received', 'device_id', 'user_id', 'team_id', 'source', 'provider', 'metadata']
    attributes_fields = ['accuracy', 'latitude', 'longitude', 'altitude', 'height', 'width', 'x', 'y']
    attributes_buff = {}
    bulk = []
    path_exist = set()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        for f in self.attributes_fields:
            self.attributes_buff[f] = Attribute.objects.filter(name=f).first()

    def import_as_attributes(self, entity: Detection, unit: dict, check: bool) -> bool:
        """
        Import rest attributes of Detection to DetectionAttribute model.

        Performance optimizations:
        - bulk insertion for new rows, bulk stored in self.bulk object field
        - if /?nocheck=1 then no checked existing row
        - cache of path existing in self.path_exist object field
        """
        changed = False
        user = self.request.user
        for f in self.attributes_fields:
            filters = {
                'detection': entity,
                'attribute': self.attributes_buff[f],
                'author': user
            }

            da = DetectionAttribute.objects.filter(**filters).first() if check else None  # type: Optional[DetectionAttribute]
            rv = unit.get(f)
            if rv is None:
                if da is not None:
                    changed = True
                    da.delete()
            else:
                v = float(rv)
                if da is None:
                    changed = True
                    self.bulk.append(DetectionAttribute(**filters, value=v))
                else:
                    changed = da.value != v
                    if changed:
                        da.value = v
                        da.save()

            frame_content = unit.get('frame_content')
            fn = entity.get_filename()
            if frame_content:
                decoded = base64.decodebytes(str.encode(frame_content))
                path = entity.get_filepath()
                if path not in self.path_exist and not os.path.exists(path):
                    os.makedirs(path)
                    self.path_exist.add(path)

                write_file = False
                if check and os.path.exists(fn):
                    data = open(fn, "rb").read()
                    if data != decoded:
                        write_file = True
                        open(fn, "wb").write(decoded)
                else:
                    write_file = True

                if write_file:
                    changed = True
                    open(fn, "wb").write(decoded)
            else:
                if os.path.exists(fn):
                    changed = True
                    os.remove(fn)

        return changed

    def bulk_attributes(self):
        if len(self.bulk):
            DetectionAttribute.objects.bulk_create(self.bulk)
            self.bulk = []
