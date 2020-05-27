from typing import List, Dict, Tuple, Optional, Callable

from hit_analysis.commons.consts import CLASSIFIED, CLASS_ARTIFACT, X, Y, ARTIFACT_NEAR_HOT_PIXEL2
from hit_analysis.commons.utils import point_to_point_distance, get_and_set
from hit_analysis.commons.grouping import group_by_resolution


def near_hot_pixel_classify2(detections: List[dict], often: int, distance: float) -> None:
    """
    Classify detections as artifact when count in group is grater or equal than often param.
    When detection was classified as artifact then 'classified' field will be set to 'artifact'
    and 'artifact_near_hot_pixel2' will be set to count of hot pixels in distance radius
    :param detections: list of detections
    :param often: when len(group) is grater or equal than often param then it will be classified as artifact
    :param distance: distance in px to near pixel
    """
    hot_pixels = {}

    # 1st pass: search all pixels
    for d in detections:
        key = (d.get(X), d.get(Y))
        get_and_set(hot_pixels, key, 0)
        hot_pixels[key] += 1

    # 2nd pass: count neighborhood hot pixels, O(n²) per device per resolution
    for d in detections:
        neighborhood = 0
        for (x, y), c in hot_pixels.items():
            if point_to_point_distance((d.get(X), d.get(Y)), (x, y)) < distance:
                neighborhood += c
        d[ARTIFACT_NEAR_HOT_PIXEL2] = neighborhood

        if neighborhood >= often:
            d[CLASSIFIED] = CLASS_ARTIFACT


def group_for_near_hot_pixel2(detections: List[dict], exclusion: Optional[Callable[[dict], bool]] = None) -> Dict[Tuple[int, int], List[dict]]:
    """
    Group detections by resolution
    :param detections: ungrouped detections, should be list of detections for one device
    :param exclusion: when is not None and return True then object will be ignored
    :return: detections grouped by resolution
    """
    return group_by_resolution(detections, exclusion)


def near_hot_pixel_process2(groups: Dict[Tuple[int, int], List[dict]], often: int = 3, distance: float = 5) -> None:
    """
    Execute hot_pixel_filter for all groups.
    :param groups: detections grouped by group_for_near_hot_pixel2
    :param often: parameter for hot_pixel_classify
    :param distance: distance in px to near pixel
    """
    for k, v in groups.items():
        near_hot_pixel_classify2(v, often, distance)
