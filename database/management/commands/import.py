import base64
from sys import stdin
import pathlib
from io import StringIO, BytesIO
import json
from PIL import Image

from typing import Any, List

from django.core.management import BaseCommand

from database.models import Detection


def decode_base64(frame_content: str) -> bytes:
    return base64.decodebytes(str.encode(frame_content))


def load_image(frame_decoded: bytes) -> Image:
    return Image.open(BytesIO(frame_decoded))


def get_and_set(obj: dict, key: Any, default: Any) -> Any:
    o = obj.get(key, default)
    obj[key] = o
    return o


def store_png(path: List[str], _id: int, frame_decoded: bytes) -> None:
    # TODO: configurable PNG storage (yes/no) and destination directory
    dirs = '/'.join(path)
    p = "/tmp/hits/%s" % dirs
    fn = '%s/%d.png' % (p, _id)
    pathlib.Path(p).mkdir(parents=True, exist_ok=True)
    with open(fn, 'wb') as f:
        f.write(frame_decoded)


def get_resolution_key(d: dict) -> str:
    return '%dx%d' % (d.get('width'), d.get('height'))


def get_xy_key(d: dict) -> str:
    return '%dx%d' % (d.get('x'), d.get('y'))


def append_to_frame(image: Image, detection: dict):
    hit_img = load_image(detection.get('frame_decoded'))
    # hit_img.save('/tmp/%d_orig.png' % detection.get('id'))
    width = hit_img.size[0]
    height = hit_img.size[1]
    x = detection.get('x')
    y = detection.get('y')

    gray = hit_img.convert('L')
    # mask = gray.point(lambda p: 0 if p == 0 else 255)

    mg = 0
    fx = 0
    fy = 0

    for cy in range(height):
        for cx in range(width):
            g = gray.getpixel((cx, cy))
            if mg < g:
                mg = g
                fx = cx
                fy = cy

    image.paste(hit_img, (x - fx, y - fy, x - fx + width, y - fy + height))  # , mask)
    image.paste(image.crop((x - fx + width - 1, y - fy, x - fx + width, y - fy + height)), (x - fx + width, y - fy, x - fx + width + 1, y - fy + height))
    image.paste(image.crop((x - fx, y - fy + height - 1, x - fx + width, y - fy + height)), (x - fx, y - fy + height, x - fx + width, y - fy + height + 1))
    image.paste(image.crop((x - fx + width - 1, y - fy + height - 1, x - fx + width, y - fy + height)), (x - fx + width, y - fy + height, x - fx + width + 1, y - fy + height + 1))
    detection['crop_x'] = x - fx
    detection['crop_y'] = y - fy
    detection['crop_size'] = (width, height)


def replace_from_frame(image: Image, detection: dict):
    x = detection.get('crop_x')
    y = detection.get('crop_y')
    w, h = detection.get('crop_size')
    hit_img = image.crop((x, y, x + w, y + h))
    with BytesIO() as output:
        hit_img.save(output, format="png")
        # hit_img.save('/tmp/%d.png' % detection.get('id'))
        detection['frame_decoded'] = output.getvalue()


class Command(BaseCommand):
    help = 'Create and initialize admin user and init build-in attributes'

    by_device_and_minute = {}  # store objects by device and detection minute and timestamp
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
        obj['frame_decoded'] = decode_base64(obj.get('frame_content'))

        # divide hits by device_id and detection minute
        device_id = obj.get('device_id')
        timestamp = obj.get('timestamp')
        minute = timestamp // 60000  # extract minute of detection
        bd = get_and_set(self.by_device_and_minute, device_id, {})  # get minutes dict by device
        bm = get_and_set(bd, minute, {})  # get hits dicts by minute
        bt = get_and_set(bm, timestamp, [])  # get hits array by timestamp
        bt.append(obj)  # append hit to device and minute

    def parse_hits(self) -> None:
        """
        Postprocess of imported hits. Simple artifact exclusion and import to database.
        """

        bulk = []  # type: List[Detection]  # TODO: for bulk insertion
        hot_pixels = {}  # counting the same XY by device_id, frame size, X value and Y value

        # build: hot_pixels
        for kd, v in self.by_device_and_minute.items():
            hpd = {}
            for km, minute in v.items():
                for kt, timestamp in minute.items():
                    for d in timestamp:
                        r = get_and_set(hpd, get_resolution_key(d), {})
                        xyk = get_xy_key(d)
                        r[xyk] = r.get(xyk, 0) + 1
            hot_pixels[kd] = hpd

        # build: bulk
        for kd, v in self.by_device_and_minute.items():
            hpd = hot_pixels[kd]
            for km, minute in v.items():
                for kt, timestamp in minute.items():
                    # fix: the fill by black cropped frame in CREDO Detector app v2
                    if len(timestamp) > 1:
                        image = Image.new('RGBA', (timestamp[0].get('width'), timestamp[0].get('height')), (0, 0, 0))
                        for d in reversed(timestamp):
                            append_to_frame(image, d)
                        for d in timestamp:
                            replace_from_frame(image, d)
                        # image.save('/tmp/test.png')
                    for d in timestamp:
                        rk = get_resolution_key(d)
                        xyk = get_xy_key(d)

                        if len(minute) >= 10:
                            store_png(['rejected', 'by_too_often', str(kd), str(km)], d.get('id'), d.get('frame_decoded'))
                            store_png(['rejected', 'by_too_often'], d.get('id'), d.get('frame_decoded'))
                        elif hpd[rk][xyk] >= 3:
                            store_png(['rejected', 'by_hot_pixel', str(kd), rk, xyk], d.get('id'), d.get('frame_decoded'))
                            store_png(['rejected', 'by_hot_pixel'], d.get('id'), d.get('frame_decoded'))
                        else:
                            if len(minute) > 1:
                                store_png(['suspicious', 'by_too_often', str(kd), str(km)], d.get('id'), d.get('frame_decoded'))
                                store_png(['suspicious', 'by_too_often'], d.get('id'), d.get('frame_decoded'))
                            elif hpd[rk][xyk] > 1:
                                store_png(['suspicious', 'by_hot_pixel', str(kd), rk, xyk], d.get('id'), d.get('frame_decoded'))
                                store_png(['suspicious', 'by_hot_pixel'], d.get('id'), d.get('frame_decoded'))
                            else:
                                store_png(['accepted', str(kd)], d.get('id'), d.get('frame_decoded'))
                                store_png(['accepted'], d.get('id'), d.get('frame_decoded'))
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
