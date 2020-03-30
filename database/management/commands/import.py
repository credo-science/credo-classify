from typing import Any, List, Tuple, Optional

import base64
import time
from sys import stdin
import pathlib
from io import StringIO, BytesIO
import json
from PIL import Image

from django.core.management import BaseCommand

from database.models import Detection


def print_log(content: str, timer: Optional[float] = None) -> float:
    t = time.time()
    if timer is not None:
        print('%s (time: %.3fs)' % (content, t - timer))
    else:
        print(content)
    return t


def decode_base64(frame_content: str) -> bytes:
    return base64.decodebytes(str.encode(frame_content))


def load_image(frame_decoded: bytes) -> Image:
    return Image.open(BytesIO(frame_decoded))


def get_and_set(obj: dict, key: Any, default: Any) -> Any:
    o = obj.get(key, default)
    obj[key] = o
    return o


def join_tuple(tpl: Tuple[int, int]) -> str:
    return '%dx%d' % tpl


def store_png(root: str, path: List[str], name: Any, frame_decoded: bytes) -> None:
    dirs = '/'.join(path)
    p = "%s/%s" % (root, dirs)
    fn = '%s/%s.png' % (p, str(name))
    pathlib.Path(p).mkdir(parents=True, exist_ok=True)
    with open(fn, 'wb') as f:
        f.write(frame_decoded)


def get_resolution_key(d: dict) -> Tuple[int, int]:
    return d.get('width'), d.get('height')


def get_xy_key(d: dict) -> Tuple[int, int]:
    return d.get('x'), d.get('y')


def point_to_point_distance(p1: Tuple[int, int], p2: Tuple[int, int]):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5


def get_near_xy_key(keys: List[Tuple[int, int]], d: dict, distance: float) -> Tuple[int, int]:
    x = d.get('x')
    y = d.get('y')
    for k in keys:
        if point_to_point_distance(k, (x, y)) < distance:
            return k
    return x, y


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

    if width == height:
        fx = width // 2
        fy = height // 2
    else:
        detection['edge'] = True
        for cy in range(height):
            for cx in range(width):
                g = gray.getpixel((cx, cy))
                if mg < g:
                    mg = g
                    fx = cx
                    fy = cy

    image.paste(hit_img, (x - fx, y - fy, x - fx + width, y - fy + height))  # , mask)

    # fix bug in early CREDO Detector App: black filled boundary 1px too large
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


def parse_pixel(pixel: Tuple[int, int, int, int]) -> int:
    r, g, b, a = pixel
    return max([r, g, b])


class Command(BaseCommand):
    # TODO: extract hit analysis code to separated file (or module installed by PIP)
    help = 'Create and initialize admin user and init build-in attributes'

    by_device_and_minute = {}  # store objects by device and detection minute and timestamp
    datatype = None
    out_dir = None

    def add_arguments(self, parser):
        parser.add_argument('-d', '--datatype', help='data to import from input: users, devices, teams, hits or pings')
        parser.add_argument('-o', '--out-dir', help='path to store debug data. For hits: png files accepterd, rejected and suspicious (but inserted)', default='')

    def store_png(self, path: List[str], name: Any, frame_decoded: bytes) -> None:
        if self.out_dir:
            store_png(self.out_dir, path, name, frame_decoded)

    def simple_classify(self, detection: dict):
        detection['class'] = 'unclassified'

        hit_img = load_image(detection.get('frame_decoded')).convert('RGBA')
        width, height = hit_img.size

        darkness = 255
        brightest = 0
        for cy in range(height):
            for cx in range(width):
                g = parse_pixel(hit_img.getpixel((cx, cy)))
                if g != 0:
                    brightest = max(brightest, g)
                    darkness = min(darkness, g)

        cut_off_darkness = 50

        if brightest - darkness <= cut_off_darkness:
            detection['class'] = 'artifact'
            detection['class_kind'] = 'dark'

        area_threshold = (brightest - darkness) / 4 + darkness

        bright_count = 0
        for cy in range(height):
            for cx in range(width):
                g = parse_pixel(hit_img.getpixel((cx, cy)))
                if g > area_threshold:
                    bright_count += 1

        bp = bright_count * 1000 / (width * height)
        if bp > 30:
            detection['class'] = 'artifact'
            detection['class_kind'] = 'area'

        self.store_png(['classify', detection['class']], '%d_d%d_b%d_diff%d_t%d' % (detection.get('id'), darkness, brightest, (brightest - darkness), bp), detection.get('frame_decoded'))
        # TODO: classify by spot, track, worm and multi by shape analysis


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
        near_hot_pixels = {}  # counting the near XY by device_id, frame size, X value and Y value

        # build: hot_pixels and near_hot_pixels
        timing = print_log('Build hot pixel map...')
        for kd, v in self.by_device_and_minute.items():
            hpd = {}
            near_hpd = {}
            for km, minute in v.items():
                for kt, timestamp in minute.items():
                    for d in timestamp:
                        rk = get_resolution_key(d)
                        r = get_and_set(hpd, rk, {})
                        xyk = get_xy_key(d)
                        r[xyk] = r.get(xyk, 0) + 1

                        near_r = get_and_set(near_hpd, rk, {})
                        near_xyk = get_near_xy_key(near_r.keys(), d, 5)
                        near_r[near_xyk] = near_r.get(near_xyk, 0) + 1
                        d['near_xyk'] = near_xyk

            hot_pixels[kd] = hpd
            near_hot_pixels[kd] = near_hpd
        print_log('... hot pixel map done', timing)

        # reconstruction the fill by black cropped frame in CREDO Detector app v2
        timing = print_log('Reconstruction cleaned image area after cutoff another hit in the same image frame (CREDO Detector app issue)...')
        for kd, v in self.by_device_and_minute.items():
            for km, minute in v.items():
                for kt, timestamp in minute.items():
                    if len(timestamp) > 1:
                        image = Image.new('RGBA', (timestamp[0].get('width'), timestamp[0].get('height')), (0, 0, 0))
                        edge = 'no_edge'
                        for d in timestamp:
                            if d.get('edge'):
                                edge = 'edge'
                        for d in reversed(timestamp):
                            frame_decoded = d.get('frame_decoded')
                            append_to_frame(image, d)
                            self.store_png(['recostruct', edge, str(kd), str(kt), 'orig'], d.get('id'), frame_decoded)
                        for d in timestamp:
                            replace_from_frame(image, d)
                            self.store_png(['recostruct', edge, str(kd), str(kt)], d.get('id'), d.get('frame_decoded'))
                        if self.out_dir:
                            image.save('%s/recostruct/%s/%d/%d/frame.png' % (self.out_dir, edge, kd, kt))
        print_log('... reconstruction done', timing)

        # build: bulk
        timing = print_log('Filter artifacts by too often and hot pixels...')
        for kd, v in self.by_device_and_minute.items():
            hpd = hot_pixels[kd]
            near_hpd = near_hot_pixels[kd]
            for km, minute in v.items():
                for kt, timestamp in minute.items():
                    for d in timestamp:
                        rk = get_resolution_key(d)
                        rk_str = join_tuple(rk)

                        xyk = get_xy_key(d)
                        xyk_str = join_tuple(xyk)
                        near_xyk = d.get('near_xyk')
                        near_xyk_str = join_tuple(near_xyk)

                        if hpd[rk][xyk] >= 3:
                            self.store_png(['rejected', 'by_hot_pixel', str(kd), rk_str, xyk_str], d.get('id'), d.get('frame_decoded'))
                            self.store_png(['rejected', 'by_hot_pixel', 'by_count', str(hpd[rk][xyk])], d.get('id'), d.get('frame_decoded'))
                        elif near_hpd[rk][near_xyk] >= 3:
                            self.store_png(['rejected', 'by_near_hot_pixel', str(kd), rk_str, near_xyk_str], d.get('id'), d.get('frame_decoded'))
                            self.store_png(['rejected', 'by_near_hot_pixel', 'by_count', str(near_hpd[rk][near_xyk])], d.get('id'), d.get('frame_decoded'))
                        elif len(minute) >= 4:
                            self.store_png(['rejected', 'by_too_often', str(kd), str(km)], d.get('id'), d.get('frame_decoded'))
                            self.store_png(['rejected', 'by_too_often', 'by_count', str(len(minute))], d.get('id'), d.get('frame_decoded'))
                        else:
                            # if hpd[rk][xyk] > 1:
                            #     self.store_png(['suspicious', 'by_hot_pixel', str(kd), rk_str, xyk_str], d.get('id'), d.get('frame_decoded'))
                            #     self.store_png(['suspicious', 'by_hot_pixel', 'by_count', str(hpd[rk][xyk])], d.get('id'), d.get('frame_decoded'))
                            # elif near_hpd[rk][near_xyk] > 1:
                            #     self.store_png(['suspicious', 'by_near_hot_pixel', str(kd), rk_str, near_xyk_str], d.get('id'), d.get('frame_decoded'))
                            #     self.store_png(['suspicious', 'by_near_hot_pixel', 'by_count', str(near_hpd[rk][near_xyk])], d.get('id'), d.get('frame_decoded'))
                            # elif len(minute) > 1:
                            #     self.store_png(['suspicious', 'by_too_often', str(kd), str(km)], d.get('id'), d.get('frame_decoded'))
                            #     self.store_png(['suspicious', 'by_too_often', 'by_count', str(len(minute))], d.get('id'), d.get('frame_decoded'))
                            # else:
                            if True:
                                self.simple_classify(d)
                                if d.get('class') == 'artifact':
                                    self.store_png(['rejected', 'artifact', str(kd)], d.get('id'), d.get('frame_decoded'))
                                    self.store_png(['rejected', 'artifact'], d.get('id'), d.get('frame_decoded'))
                                else:
                                    self.store_png(['accepted', str(kd)], d.get('id'), d.get('frame_decoded'))
                                    self.store_png(['accepted', d.get('class')], d.get('id'), d.get('frame_decoded'))
                            # TODO: make Detection object and append to bulk[]
        print_log('... filter artifacts by too often and hot pixels done', timing)

        # TODO: insert bulk[] to database

    def handle(self, *args, **options):
        self.datatype = options['datatype']
        self.out_dir = options['out_dir']

        if self.datatype != 'hits':
            print('Other datatypes than hits is not supported yet')

        timing2 = timing = print_log('Parsing objects from JSON provided in STDIN...')
        count = 0

        stage = 0
        buff = None
        for line in stdin:
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

                        count += 1
                        if count % 10000 == 0:
                            timing2 = print_log('... just parsed %d objects...' % count, timing2)
                    else:
                        buff.write(a)

        print_log('... done, the %d objects was parsed' % count, timing)
        print('\nPostprocess of objects and insert to database:')
        if self.datatype == 'hits':
            self.parse_hits()
        print_log('... done all', timing)
