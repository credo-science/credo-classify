from hit_analysis.commons.consts import DARKNESS, BRIGHTEST, CLASSIFIED, CLASS_ARTIFACT, ARTIFACT_TOO_LARGE_BRIGHT_AREA, BRIGHTER_COUNT, IMAGE
from hit_analysis.image.image_utils import count_of_brightest_pixels


def too_large_bright_area_classify(detection: dict, threshold: int, bac: float) -> None:
    """
    Classify detections as artifact when area of brightest pixels than threshold is larger than bac param.
    :param detection: detection with 'image' and 'image_brighter_count_{threshold}' field
    :param threshold: threshold for count of pixels
    :param bac: relative quantity of brightest pixels in BAC
    """
    assert detection.get(IMAGE) is not None
    assert detection.get(BRIGHTER_COUNT % threshold) is not None

    width, height = detection.get(IMAGE).size
    area = detection.get(BRIGHTER_COUNT % threshold)

    p = area * 1000 / (width * height)

    if p > bac:
        detection[CLASSIFIED] = CLASS_ARTIFACT
        detection[ARTIFACT_TOO_LARGE_BRIGHT_AREA] = p


def too_large_bright_area(detection: dict, threshold: int, bac: float) -> None:
    """
    Classify detections as artifact when area of brightest pixels than threshold is larger than bac param.
    :param detection: detection with 'image' field
    :param threshold: threshold for count of pixels
    :param bac: relative quantity of brightest pixels in BAC
    """
    count_of_brightest_pixels(detection, threshold)
    too_large_bright_area_classify(detection, threshold, bac)
