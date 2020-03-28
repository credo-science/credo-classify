import base64
from sys import stdin
import pathlib
from io import StringIO
import json
from typing import Any, List

from django.core.management import BaseCommand

from database.models import Detection


def get_and_set(obj: dict, key: Any, default: Any) -> Any:
    o = obj.get(key, default)
    obj[key] = o
    return o


def store_png(path: List[str], _id: int, frame_content: str) -> None:
    # TODO: configurable PNG storage (yes/no) and destination directory
    dirs = '/'.join(path)
    p = "/tmp/hits/%s" % dirs
    fn = '%s/%d.png' % (p, _id)
    pathlib.Path(p).mkdir(parents=True, exist_ok=True)
    with open(fn, 'wb') as f:
        f.write(base64.decodebytes(str.encode(frame_content)))


def get_resolution_key(d: dict) -> str:
    return '%dx%d' % (d.get('width'), d.get('height'))


def get_xy_key(d: dict) -> str:
    return '%dx%d' % (d.get('x'), d.get('y'))


class Command(BaseCommand):
    help = 'Create and initialize admin user and init build-in attributes'

    by_device_and_minute = {}  # store objects by device and detection minute
    datatype = None

    def add_arguments(self, parser):
        parser.add_argument('-d', '--datatype', help='data to import from input: users, devices, teams, hits or pings')

    def parse_object(self, s: str) -> None:
        """
        The JSON stream reader callback method for one object.
        :param s: string with object data extracted form JSON file
        """
        o = json.loads(s)
        if self.datatype == 'hits':
            self.parse_hit(o)

    def parse_hit(self, obj: dict) -> None:
        """
        Parse one hit from JSON and store in self.by_device_and_minute
        :param obj: JSON object with one hit
        """

        # ignore non-image hits
        if not obj.get('frame_content'):
            return

        # divide hits by device_id and detection minute
        device_id = obj.get('device_id')
        t = obj.get('timestamp') // 60000  # extract minute of detection
        bd = get_and_set(self.by_device_and_minute, device_id, {})  # get minutes dict by device
        bt = get_and_set(bd, t, [])  # get hits array by minute
        bt.append(obj)  # append hit to device and minute

    def parse_hits(self) -> None:
        """
        Postprocess of imported hits. Simple artifact exclusion and import to database.
        """

        bulk = []  # type: List[Detection]  # TODO: for bulk insertion
        hot_pixels = {}  # counting the same XY by device_id, frame size, X value and Y value

        # build: hot_pixels
        for k, v in self.by_device_and_minute.items():
            hpd = {}
            for minute in v.values():
                for d in minute:
                    r = get_and_set(hpd, get_resolution_key(d), {})
                    xyk = get_xy_key(d)
                    r[xyk] = r.get(xyk, 0) + 1
            hot_pixels[k] = hpd

        # build: bulk
        for kd, v in self.by_device_and_minute.items():
            hpd = hot_pixels[kd]
            for km, minute in v.items():
                for d in minute:
                    rk = get_resolution_key(d)
                    xyk = get_xy_key(d)

                    if len(minute) >= 10:
                        store_png(['rejected', 'by_too_often', str(kd), str(km)], d.get('id'), d.get('frame_content'))
                        store_png(['rejected', 'by_too_often'], d.get('id'), d.get('frame_content'))
                    elif hpd[rk][xyk] >= 3:
                        store_png(['rejected', 'by_hot_pixel', str(kd), rk, xyk], d.get('id'), d.get('frame_content'))
                        store_png(['rejected', 'by_hot_pixel'], d.get('id'), d.get('frame_content'))
                    else:
                        if len(minute) > 1:
                            store_png(['suspicious', 'by_too_often', str(kd), str(km)], d.get('id'), d.get('frame_content'))
                            store_png(['suspicious', 'by_too_often'], d.get('id'), d.get('frame_content'))
                        elif hpd[rk][xyk] > 1:
                            store_png(['suspicious', 'by_hot_pixel', str(kd), rk, xyk], d.get('id'), d.get('frame_content'))
                            store_png(['suspicious', 'by_hot_pixel'], d.get('id'), d.get('frame_content'))
                        else:
                            store_png(['accepted', str(kd)], d.get('id'), d.get('frame_content'))
                            store_png(['accepted'], d.get('id'), d.get('frame_content'))
                        # TODO: make Detection object and append to bulk[]
        # TODO: insert bulk[] to database

    def handle(self, *args, **options):
        self.datatype = options['datatype']

        if self.datatype != 'hits':
            print('Other datatypes than hits is not supported yet')

        stage = 0
        buff = None
        while True:
            line = stdin.read()
            for a in line:
                if stage == 0:
                    if a == '[':
                        stage = 1
                        continue  # and read next character
                if stage == 1:
                    if a == ']':
                        break
                    if a == '{':
                        buff = StringIO()
                        stage = 2  # and continue parsing this character in stage 2
                if stage == 2:
                    if a == '}':
                        buff.write(a)
                        self.parse_object(buff.getvalue())
                        buff.close()
                        buff = None
                        stage = 1
                    else:
                        buff.write(a)
            if line == '':
                break

        if self.datatype == 'hits':
            self.parse_hits()
