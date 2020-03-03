from rest_framework.response import Response
from rest_framework.views import APIView

from classify.helpers import find_unclassified_by_user
from classify.serializers import DetectionClassifySerializer


class RandomToClassifyToken(APIView):
    def get(self, request, *args, **kwargs):
        ucs = find_unclassified_by_user(request.user)  # TODO: support filter and count
        json = map(lambda x: DetectionClassifySerializer(x).data, ucs)
        return Response({'detections': json})


random_to_classify = RandomToClassifyToken.as_view()
