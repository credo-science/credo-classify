from io import BytesIO
from typing import Tuple, Callable

from PIL import Image

from hit_analysis.commons.consts import IMAGE, FRAME_DECODED, DARKNESS, BRIGHTEST, BRIGHTER_COUNT, FRAME_CONTENT
from hit_analysis.io.io_utils import decode_base64


def get_brightest_channel(pixel: Tuple[int, int, int, int]) -> int:
    """
    Get brightest channel for pixel
    :param pixel: RGBA pixel
    :return: brightest pixel from [R, G, B] list
    """
    r, g, b, a = pixel
    return max([r, g, b])


def load_image(detection: dict) -> Image:
    """
    Load image from 'frame_encoded' or 'frame_content' field to 'image' field and return.
    When 'frame_encoded' field is None then will be filled by decode the 'frame_content' field.
    :param detection: detection with 'frame_encoded' or 'frame_content
    :return: image object
    """
    if detection.get(FRAME_DECODED) is None:
        detection[FRAME_DECODED] = decode_base64(detection.get(FRAME_CONTENT))

    frame_decoded = detection.get(FRAME_DECODED)
    img = Image.open(BytesIO(frame_decoded)).convert('RGBA')
    detection[IMAGE] = img
    return img


def measure_darkness_brightest(detection: dict, pixel_parser: Callable[[Tuple[int, int, int, int]], int] = get_brightest_channel) -> Tuple[int, int]:
    """
    Measure brightest and darkness pixel excluding #000 pixels and using pixel_parser for get pixel value.
    Set values to 'image_darkness' and 'image_brightest' fields and return.
    :param detection: detection with 'image' field
    :param pixel_parser: get one value from RGBA channels
    :return: tuple of darkness and brightest
    """
    assert detection.get(IMAGE) is not None

    hit_img = detection.get(IMAGE)
    width, height = hit_img.size

    darkness = 255
    brightest = 0
    for cy in range(height):
        for cx in range(width):
            g = pixel_parser(hit_img.getpixel((cx, cy)))
            if g != 0:
                brightest = max(brightest, g)
                darkness = min(darkness, g)
    detection[DARKNESS] = darkness
    detection[BRIGHTEST] = brightest
    return darkness, brightest


def count_of_brightest_pixels(detection: dict, threshold: int, pixel_parser: Callable[[Tuple[int, int, int, int]], int] = get_brightest_channel) -> int:
    """
    Count pixels brighter than threshold param. Using pixel_parser for get pixel value.
    Set values to 'image_brighter_count_{threshold}' fields and return.
    :param detection: detection with 'image' field
    :param threshold: greater of equal bright of pixel will be counted
    :param pixel_parser: get one value from RGBA channels
    :return: count of pixel brighter or equal than threshold
    """
    assert detection.get(IMAGE) is not None

    hit_img = detection.get(IMAGE)
    width, height = hit_img.size

    bright_count = 0
    for cy in range(height):
        for cx in range(width):
            g = pixel_parser(hit_img.getpixel((cx, cy)))
            if g >= threshold:
                bright_count += 1
    detection[BRIGHTER_COUNT % threshold] = bright_count
    return bright_count


def detection_load_parser(detection: dict):
    if not detection.get(FRAME_CONTENT):
        return False
    load_image(detection)
    return True
