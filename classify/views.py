from typing import Dict

from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView

from classify.helpers import find_unclassified_by_user
from classify.models import Classified
from classify.serializers import DetectionClassifySerializer
from definitions.models import Attribute
from users.models import User
from users.serializers import UserViewSerializer
from values.models import DetectionAttribute


class RandomToClassifyToken(APIView):
    def get_next_to_classify(self):
        ucs = find_unclassified_by_user(self.request.user)  # TODO: support filter and count
        user = self.request.user
        if len(ucs) == 1:
            return Response({
                'user': UserViewSerializer(user).data,
                'detection': DetectionClassifySerializer(ucs[0]).data
            })
        else:
            return Response(status=404)

    def get(self, request, *args, **kwargs):
        return self.get_next_to_classify()

    def post(self, request, *args, **kwargs):
        data = request.data
        detection_id = data.get('id')
        classes = data.get('classes')  # type: Dict[str, int]
        user = request.user

        points = 0

        for k, v in classes.items():
            a = DetectionAttribute.objects.filter(
                detection_id=detection_id, author=user, attribute__name=k
            ).first()  # type: DetectionAttribute
            if a is None:
                DetectionAttribute.objects.create(
                    detection_id=detection_id, author=user, attribute=Attribute.objects.get(name=k), value=v
                )
                points += 1
            else:
                a.value = v
                a.save()

        if len(classes.keys()):
            c = Classified.objects.filter(user=user, detection_id=detection_id).first()
            if c is None:
                Classified.objects.create(user=user, detection_id=detection_id)

        user.score += points
        User.objects.filter(username=user.username).update(score=F('score') + points)

        return self.get_next_to_classify()


random_to_classify = RandomToClassifyToken.as_view()
