from commons.serialization import SafeModelViewSet
from definitions.models import Attribute
from definitions.serializers import AttributeSerializer


class AttributeViewSet(SafeModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filterset_fields = '__all__'
