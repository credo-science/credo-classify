from typing import List, Dict, Tuple, Optional, Callable

from hit_analysis.commons.consts import CLASSIFIED, CLASS_ARTIFACT, X, Y, ARTIFACT_NEAR_HOT_PIXEL, ARTIFACT_NEAR_HOT_PIXEL_REFXY
from hit_analysis.commons.utils import point_to_point_distance
from hit_analysis.commons.grouping import group_by_lambda, group_by_resolution


def get_near_xy_key(keys: List[Tuple[int, int]], detection: dict, distance: float) -> Tuple[int, int]:
    """
    Get first nearer than distance param from keys or new (X,Y) key.
    :param keys: list of used keys
    :param detection: detection
    :param distance: distance in px to near pixel
    :return: existing key from keys or new key
    """
    x = detection.get(X)
    y = detection.get(Y)
    for k in keys:
        if point_to_point_distance(k, (x, y)) < distance:
            return k
    return x, y


def near_hot_pixel_classify(group: Dict[Tuple[int, int], List[dict]], often: int, key: Tuple[int, int]) -> None:
    """
    Classify detections as artifact when count in group is grater or equal than often param.
    When detection was classified as artifact then 'classified' field will be set to 'artifact'
    and 'artifact_near_hot_pixel' will be set to len(group)
    :param group: list of detections grouped by near_XY of detection
    :param often: when len(group) is grater or equal than often param then it will be classified as artifact
    :param key: reference X and Y, stored in artifact_near_hot_pixel_refxy when classified as artifact
    """
    for detections in group.values():
        count = len(detections)
        if count >= often:
            for d in detections:
                d[CLASSIFIED] = CLASS_ARTIFACT
                d[ARTIFACT_NEAR_HOT_PIXEL] = count
                d[ARTIFACT_NEAR_HOT_PIXEL_REFXY] = key


def group_for_near_hot_pixel(detections: List[dict], distance: float, exclusion: Optional[Callable[[dict], bool]] = None) -> Dict[Tuple[int, int], Dict[Tuple[int, int], List[dict]]]:
    """
    Group detections by resolution and XY of detection
    :param detections: ungrouped detections, should be list of detections for one device
    :param distance: distance in px to near pixel
    :param exclusion: when is not None and return True then object will be ignored
    :return: detections grouped by resolution and XY of detection
    """
    grouped = group_by_resolution(detections, exclusion)
    ret = {}
    for k, g in grouped.items():
        r = group_by_lambda(g, lambda x, y: get_near_xy_key(y, x, distance))
        if len(r.keys()) > 0:
            ret[k] = r
    return ret


def near_hot_pixel_process(groups: Dict[Tuple[int, int], Dict[Tuple[int, int], List[dict]]], often: int = 3) -> None:
    """
    Execute hot_pixel_filter for all groups.
    :param groups: detections grouped by group_for_hot_pixel
    :param often: parameter for hot_pixel_classify
    """
    for k, v in groups.items():
        near_hot_pixel_classify(v, often, k)
