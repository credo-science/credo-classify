from typing import List

from django.db.models import QuerySet, F

from classify.models import DetectionScore
from database.models import Detection
from users.models import User


def find_unclassified_by_user(user: User, kind: str, count=1, own_qs: QuerySet = None) -> List[Detection]:
    """
    List of hits to classify (excluding just classified)
    :param user: for filter unclassified by user
    :param kind: kind of classification, @see Attribute.kind
    :param count: count hits to get
    :param own_qs: filtered queryset of hits
    :return: list of unclassified hits
    """
    ret = []
    tries = 100  # TODO: find better solution for select from Detection without related Score entity
    uqs = Detection.objects.all() if own_qs is None else own_qs

    while len(ret) < count and tries > 0:
        ids = []
        qs = uqs.filter(has_image=True).order_by('score', 'random')[:count]

        for d in qs:
            if not DetectionScore.has(user, d, kind):
                ret.append(d)
                ids.append(d.id)
            if len(ret) >= count:
                break

        Detection.objects.filter(id__in=ids).update(score=F('score') + 1)
        tries -= 1

    return ret
