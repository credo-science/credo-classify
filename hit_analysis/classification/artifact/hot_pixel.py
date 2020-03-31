from typing import List, Dict, Tuple, Optional, Callable

from hit_analysis.commons.consts import CLASSIFIED, CLASS_ARTIFACT, ARTIFACT_HOT_PIXEL
from hit_analysis.commons.utils import get_xy_key
from hit_analysis.commons.grouping import group_by_lambda, group_by_resolution


def hot_pixel_classify(group: Dict[Tuple[int, int], List[dict]], often: int) -> None:
    """
    Classify detections as artifact when count in group is grater or equal than often param.
    When detection was classified as artifact then 'classified' field will be set to 'artifact'
    and 'artifact_hot_pixel' will be set to len(group)
    :param group: list of detections grouped by XY of detection
    :param often: when len(group) is grater or equal than often param then it will be classified as artifact
    """
    count = len(group.keys())
    if count >= often:
        for detections in group.values():
            for d in detections:
                d[CLASSIFIED] = CLASS_ARTIFACT
                d[ARTIFACT_HOT_PIXEL] = count


def group_for_hot_pixel(detections: List[dict], exclusion: Optional[Callable[[dict], bool]] = None) -> Dict[Tuple[int, int], Dict[Tuple[int, int], List[dict]]]:
    """
    Group detections by resolution and XY of detection
    :param detections: ungrouped detections
    :param exclusion: when is not None and return True then object will be ignored
    :return: detections grouped by resolution and XY of detection
    """
    grouped = group_by_resolution(detections, exclusion)
    ret = {}
    for k, g in grouped.items():
        r = group_by_lambda(g, lambda x, y: get_xy_key(x))
        if len(r.keys()) > 0:
            ret[k] = r
    return ret


def hot_pixel_process(groups: Dict[Tuple[int, int], Dict[Tuple[int, int], List[dict]]], often: int = 3) -> None:
    """
    Execute hot_pixel_filter for all groups.
    :param groups: detections grouped by group_for_hot_pixel
    :param often: parameter for hot_pixel_classify
    """
    for k, v in groups.items():
        hot_pixel_classify(v, often)
