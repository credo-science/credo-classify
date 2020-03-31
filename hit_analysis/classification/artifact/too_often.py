from typing import List, Dict, Optional, Callable

from hit_analysis.commons.consts import CLASSIFIED, CLASS_ARTIFACT, ARTIFACT_TOO_OFTEN
from hit_analysis.commons.grouping import group_by_timestamp_division


def too_often_classify(group: Dict[int, List[dict]], often: int) -> None:
    """
    Classify detections as artifact when count in group is grater or equal than often param.
    When detection was classified as artifact then 'classified' field will be set to 'artifact'
    and 'artifact_too_often' will be set to len(group)
    :param group: list of detections grouped by timestamp
    :param often: when len(group) is grater or equal than often param then it will be classified as artifact
    """
    count = len(group.keys())
    if count >= often:
        for detections in group.values():
            for d in detections:
                d[CLASSIFIED] = CLASS_ARTIFACT
                d[ARTIFACT_TOO_OFTEN] = count


def group_for_too_often(detections: List[dict], time_division: int = 60000, exclusion: Optional[Callable[[dict], bool]] = None) -> Dict[int, Dict[int, List[dict]]]:
    """
    Group detections for too_often_filter.
    :param detections: ungrouped list of detections
    :param time_division: time window for division in ms, default 60000ms = 1 minute
    :param exclusion: when is not None and return True then object will be ignored
    :return: list of detection grouped by time_division then timestamp
    """
    grouped = group_by_timestamp_division(detections, time_division, exclusion)
    ret = {}
    for k, v in grouped.values():
        r = group_by_timestamp_division(v, 1)
        if len(r.keys()) > 0:
            ret[k] = r
    return ret


def too_often_process(groups: Dict[int, Dict[int, List[dict]]], often: int = 4) -> None:
    """
    Execute too_often_filter for all groups.
    :param groups: detections grouped by group_for_too_often
    :param often: parameter for too_often_filter
    """
    for k, v in groups.items():
        too_often_classify(v, often)
