import random
from typing import List

from django.db.models import QuerySet

from classify.models import Classified
from database.models import Detection
from users.models import User


def find_unclassified_by_user(user: User, count=1, qs: QuerySet = None) -> List[Detection]:
    ret = []
    used = set()

    qs = qs or Detection.objects.all()
    entities = qs.count()

    tries = 100  # TODO: need to optimize unclassified detections (maybe fast bitmap cache)

    while len(used) < count and tries > 0:
        nr = random.randint(0, entities)
        d = qs[nr]  # type: Detection  # TODO: it is slow method :(
        if Classified.objects.filter(user=user, detection=d).count() == 0:
            used.add(nr)
            ret.append(d)
        else:
            tries -= 1

    return ret
