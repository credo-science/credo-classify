from typing import Dict

from rest_framework.response import Response
from rest_framework.views import APIView

from classify.helpers import find_unclassified_by_user
from classify.models import DetectionScore
from classify.serializers import DetectionClassifySerializer
from database.models import Detection
from users.serializers import UserViewSerializer
from values.models import DetectionAttribute


class BaseRandomToClassify(APIView):
    kind = None

    def get_filtered_hits(self):
        user = self.request.query_params.get('user', '')
        team = self.request.query_params.get('team', '')
        qs = Detection.objects.all()
        if user:
            qs = qs.filter(user_id=user)
        if team:
            qs = qs.filter(team_id=team)
        return qs

    def get_next_to_classify(self):
        user = self.request.user
        count = int(self.request.query_params.get('count', '1'))
        ucs = find_unclassified_by_user(user, self.kind, min(count, 100), self.get_filtered_hits())
        if len(ucs) == 1:
            return Response({
                'user': UserViewSerializer(user).data,
                'detection': DetectionClassifySerializer(ucs[0]).data
            })
        else:
            return Response(status=404)

    def get(self, request, *args, **kwargs):
        return self.get_next_to_classify()


class RandomToClassifyOne(BaseRandomToClassify):
    kind = 'co'

    def post(self, request, *args, **kwargs):
        data = request.data
        detection_id = data.get('id')
        name = data.get('attribute')
        value = data.get('value')
        user = request.user

        ret, created = DetectionAttribute.set_or_update_value(
            detection_id=detection_id,
            user=user,
            attribute=name,
            value=value
        )

        user.fast_update_scores(*DetectionScore.set_new_points(user, ret.detection, 'co', 1))
        return self.get_next_to_classify()


random_to_classify_one  = RandomToClassifyOne.as_view()


class RandomToClassifyScaled(BaseRandomToClassify):
    kind = 'cs'

    def post(self, request, *args, **kwargs):
        data = request.data
        detection_id = data.get('id')
        classes = data.get('classes')  # type: Dict[str, int]
        user = request.user

        points = 0
        detection = None

        for k, v in classes.items():
            ret, created = DetectionAttribute.set_or_update_value(
                detection_id=detection_id,
                user=user,
                attribute=k,
                value=v
            )
            detection = ret.detection

        if len(classes.keys()) and detection is not None:
            user.fast_update_scores(*DetectionScore.set_new_points(user, detection, 'cs', points))
        return self.get_next_to_classify()


random_to_classify_scaled = RandomToClassifyScaled.as_view()


class RandomToClassifySelect(BaseRandomToClassify):
    kind = 'co'

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get('attribute')
        value = data.get('value')
        detections = data.get('detections')
        user = request.user

        us = 0
        uv = 0

        for detection_id in detections:
            ret, created = DetectionAttribute.set_or_update_value(
                detection_id=detection_id,
                user=user,
                attribute=name,
                value=value
            )

            s, v = DetectionScore.set_new_points(user, ret.detection, 'co', 1)
            us += s
            uv += v

        user.fast_update_scores(us, uv)
        return self.get_next_to_classify()


random_to_classify_select = RandomToClassifySelect.as_view()
