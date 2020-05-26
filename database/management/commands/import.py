from random import randrange
from sys import stdin
from typing import List, Tuple

from django.core.management import BaseCommand
from django.db import transaction

from database.models import Team, Device, CredoUser, Detection
from hit_analysis.batch.load_detections import analyse_detections_batch
from hit_analysis.commons.config import Config
from hit_analysis.commons.consts import CLASS_ARTIFACT
from hit_analysis.image.image_utils import detection_load_parser
from hit_analysis.io.load_write import load_objects_from_stream


import_options = {
    'teams': {'cls': Team},
    'devices': {'cls': Device},
    'users': {'cls': CredoUser},
}


def sync_db(objects: List[dict], options: dict) -> Tuple[int, int, int]:
    if len(objects) == 0:
        return 0, 0, 0

    in_db = {}

    to_insert = []
    to_update = []
    not_changed = 0

    cls = options.get('cls')
    for o in cls.objects.all():
        in_db[o.id] = o

    fields = set(objects[0].keys())  # cls._meta.get_fields()
    fields_no_id = set(objects[0].keys())
    fields_no_id.remove('id')  # bulk update must be without primary key in fields list

    for o in objects:
        _id = o.get('id')
        e = in_db.get(_id)
        if e is None:
            e = cls()
            for f in fields:
                setattr(e, f, o.get(f))
            to_insert.append(e)
        else:
            changed = False
            for f in fields:
                v = o.get(f)
                if getattr(e, f) != v:
                    setattr(e, f, v)
                    changed = True
            if changed:
                to_update.append(e)
            else:
                not_changed += 1

    cls.objects.bulk_update(to_update, fields_no_id)
    cls.objects.bulk_create(to_insert)
    return len(to_insert), len(to_update), not_changed


def insert_detections(objects: List[dict]) -> int:
    to_insert = []

    for o in objects:
        d = Detection()
        for f in [
            'id',
            'device_id',
            'user_id',
            'team_id',
            'timestamp',
            'time_received',
            'source',
            'provider',
            'metadata',

            'width',
            'height',

            'x',
            'y',
            'latitude',
            'longitude',
            'altitude',
            'accuracy',
        ]:
            setattr(d, f, o.get(f))

        d.has_image = o.get('image') is not None
        if d.has_image:
            d.frame_content = o.get('frame_decoded')
            d.detection_width, d.detection_height = o.get('image').size
            d.mime = 'image/png'  # TODO: get from frame_content header
            d.detection_inner = d.detection_width == d.detection_inner
            d.ml_class = 4 if o.get('classified') == CLASS_ARTIFACT else 0
            d.ml_hot_pixel = 5 if o.get('artifact_hot_pixel') > 1 else 1
        d.random = randrange(-2147483648, 2147483647)

        to_insert.append(d)

    Detection.objects.bulk_create(to_insert)
    return len(to_insert)


class Command(BaseCommand):
    help = 'Create and initialize admin user and init build-in attributes'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--datatype', help='data to import from input: users, devices, teams, hits or pings')
        parser.add_argument('-o', '--out-dir', help='path to store debug data. For hits: png files accepterd, rejected and suspicious (but inserted)', default='')
        parser.add_argument('-i', '--input-file', help='input JSON file, default: stdin', default='-')

    def handle(self, *args, **options):
        datatype = options['datatype']
        out_dir = options['out_dir']
        input_file = options['input_file']

        if datatype != 'hits':
            print('Other datatypes than hits is not supported yet')

        config = Config(out_dir)
        inp = stdin if input_file == '-' else open(input_file, 'r')

        if datatype == 'hits':
            objects = load_objects_from_stream(inp, config, detection_load_parser)
            analyse_detections_batch(objects, config)
            inserted = insert_detections(objects)
            print('Inserted %d detections' % inserted)
        elif datatype in import_options.keys():
            objects = load_objects_from_stream(inp, config)
            inserted, updated, not_changed = sync_db(objects, import_options.get(datatype))
            print('Objects %s importing finish, inserted: %d, updated: %d, not changed: %d' % (datatype, inserted, updated, not_changed))

        if input_file != '-':
            inp.close()
