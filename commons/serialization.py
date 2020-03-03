from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet


def get_safe_query_set(q: QuerySet, action: str) -> QuerySet:
    if action in ['list', 'retrive', 'check', 'summary']:
        return q
    return q.select_for_update()


class SafeModelViewSet(ModelViewSet):
    def get_queryset(self) -> QuerySet:
        return get_safe_query_set(super().get_queryset(), self.action)
