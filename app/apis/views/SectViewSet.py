from rest_framework import viewsets
from core.models import Sect
from apis.serializers import SectSerializer


class SectViewSet(viewsets.ModelViewSet):
    serializer_class = SectSerializer

    def get_queryset(self):
        queryset = Sect.objects.all()
        return queryset
