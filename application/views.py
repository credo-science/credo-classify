from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from application.models import Team
from application.serializers import TeamsFileSerializer


class ImportTeams(APIView):
    serializer_class = TeamsFileSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        parsed = 0
        inserted = 0
        updated = 0
        not_changed = 0

        for team in serializer.validated_data.get('teams', []):
            parsed += 1
            t_id = team.get('id')
            t_name = team.get('name')

            t = Team.objects.filter(pk=team.get('id')).first()  # type: Team
            if t is None:
                inserted += 1
                Team.objects.create(id=t_id, name=t_name)
            else:
                if t.name == t_name:
                    not_changed += 1
                else:
                    t.name = t_name
                    updated += 1
                    t.save()

        return Response({
            'parsed': parsed,
            'inserted': inserted,
            'updated': updated,
            'not_changed': not_changed
        })
