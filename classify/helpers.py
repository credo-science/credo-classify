from typing import List

from django.db.models import QuerySet, F

from classify.models import Classified
from database.models import Detection
from users.models import User


def find_unclassified_by_user(user: User, count=1, qs: QuerySet = None) -> List[Detection]:
    ret = []
    ids = []

    qs = (qs or Detection.objects.all()).filter(mime__isnull=False).order_by('score', 'random')

    for d in qs:
        if Classified.objects.filter(user=user, detection=d).count() == 0:
            ret.append(d)
            ids.append(d.id)
        if len(ret) >= count:
            break

    Detection.objects.filter(id__in=ids).update(score=F('score') + 1)

    return ret
