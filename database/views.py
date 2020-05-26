import base64
import io
from random import randrange
from typing import Any, Optional, List
from PIL import Image

from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_410_GONE
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
        - attrbulk for bulk insertion of attributes (can't use private field)
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        parsed = 0
        inserted = 0
        updated = 0
        not_changed = 0

        check = not self.nocheck_exists(request)
        bulk = []
        first = True

        for unit in serializer.validated_data.get(self.unit_name, []):
            parsed += 1
            v_id = unit.get('id')

            # quick test: when nocheck then check if first in DB and when it then raise error
            if not check and first:
                v = self.model_class.objects.filter(pk=v_id).first()
                if v is not None:
                    return Response({
                        'parsed': 0,
                        'inserted': 0,
                        'updated': 0,
                        'not_changed': 0
                    }, status=HTTP_410_GONE)
            first = False

            v_fields = {}
            for f in self.fields_to_import:
                v_fields[f] = unit.get(f)

            v = self.model_class.objects.filter(pk=v_id).first() if check else None  # type: Optional[Model]
            if v is None:
                inserted += 1
                e = self.model_class(id=v_id, **v_fields)
                self.post_import(e, unit)
                bulk.append(e)
            else:
                changed = False
                for key, value in v_fields.items():
                    if getattr(v, key) != value:
                        changed = True
                        setattr(v, key, value)

                if changed:
                    v.save()
                    updated += 1
                else:
                    not_changed += 1

        if len(bulk):
            self.model_class.objects.bulk_create(bulk)

        return Response({
            'parsed': parsed,
            'inserted': inserted,
            'updated': updated,
            'not_changed': not_changed
        })

    def post_import(self, entity, source):
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
    fields_to_import = ['timestamp', 'time_received', 'device_id', 'user_id', 'team_id', 'source', 'provider', 'metadata', 'accuracy', 'latitude', 'longitude', 'altitude', 'height', 'width', 'x', 'y']

    def post_import(self, entity: Detection, source):
        frame_content = source.get('frame_content')
        if frame_content:
            entity.has_image = True
            try:
                entity.frame_content = base64.decodebytes(str.encode(frame_content))
                image = Image.open(io.BytesIO(entity.frame_content))
                entity.mime = 'image/png'
                entity.detection_width, entity.detection_height = image.size
                entity.random = randrange(-2147483648, 2147483647)
            except:
                entity.frame_content = None
                entity.mime = None
                entity.detection_width = None
                entity.detection_height = None
        else:
            entity.has_image = False


def serve_image(request, detection_id, *args, **kwargs):
    detection = get_object_or_404(Detection, pk=detection_id)
    return HttpResponse(detection.frame_content, content_type=detection.mime)


class CheckUserTeamIdView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user')
        team = request.data.get('team')
        ret = {}
        if user:
            u = CredoUser.objects.filter(username=user).first()
            if u:
                ret['user_id'] = u.id
        if team:
            t = Team.objects.filter(name=team).first()
            if t:
                ret['team_id'] = t.id

        return Response(ret)
