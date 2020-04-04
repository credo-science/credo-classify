from io import BytesIO
from typing import List, Dict

from PIL import Image

from hit_analysis.commons.config import Config
from hit_analysis.commons.consts import IMAGE, CROP_X, CROP_Y, CROP_SIZE, FRAME_DECODED, EDGE, CLASSIFIED, CLASS_ARTIFACT


def append_to_frame(image: Image, detection: dict):
    hit_img = detection.get(IMAGE)
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
        detection[EDGE] = True
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

    detection[CROP_X] = x - fx
    detection[CROP_Y] = y - fy
    detection[CROP_SIZE] = (width, height)


def replace_from_frame(image: Image, detection: dict):
    x = detection.get(CROP_X)
    y = detection.get(CROP_Y)
    w, h = detection.get(CROP_SIZE)
    hit_img = image.crop((x, y, x + w, y + h))
    detection[IMAGE] = hit_img
    with BytesIO() as output:
        hit_img.save(output, format="png")
        # hit_img.save('/tmp/%d.png' % detection.get('id'))
        detection[FRAME_DECODED] = output.getvalue()


def do_reconstruct(detections: List[dict], config: Config) -> None:
    """
    Reconstruction the fill by black cropped frame in CREDO Detector app v2.

    The detection[x]['frame_decoded'] will be replaced by new value, old value will be stored in detection[x]['frame_decoded_orig'].

    No any changes when count of detections is less or equal 1

    :param detections: should be sorted by detection_id
    :param config: config object
    """
    if len(detections) <= 1:
        return

    sp = [str(detections[0].get('device_id')), str(detections[0].get('timestamp'))]

    image = Image.new('RGBA', (detections[0].get('width'), detections[0].get('height')), (0, 0, 0))
    edge = 'no_edge'
    for d in detections:
        if d.get('edge'):
            edge = 'edge'
    for d in reversed(detections):
        frame_decoded = d.get('frame_decoded')
        d['frame_decoded_orig'] = frame_decoded
        append_to_frame(image, d)
        config.store_png(['recostruct', edge, *sp, 'orig'], d.get('id'), frame_decoded)
    for d in detections:
        replace_from_frame(image, d)
        config.store_png(['recostruct', edge, *sp], d.get('id'), d.get('frame_decoded'))
    if config.out_dir:
        image.save('%s/recostruct/%s/%s/frame.png' % (config.out_dir, edge, "/".join(sp)))


def check_all_artifacts(detections: List[dict]) -> bool:
    """
    Check if all detections is just classified as artifacts
    :param detections: list of detections to check
    :return: True - all detections is artifacts
    """
    for d in detections:
        if d.get(CLASSIFIED) != CLASS_ARTIFACT:
            return False
    return True


def filter_unclassified(by_timestamp: Dict[int, List[dict]]) -> List[int]:
    """
    Filter detections with one or more unclassified as artifact.
    :param by_timestamp: detections grouped by timestamp
    :return: list of filtered timestamp keys
    """
    ret = []
    for timestamp, detections in by_timestamp.items():
        if not check_all_artifacts(detections):
            ret.append(timestamp)
    return ret
