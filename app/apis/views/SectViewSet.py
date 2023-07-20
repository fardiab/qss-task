from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Sect
from apis.serializers import SectSerializer


class SectViewSet(APIView):
    serializer_class = SectSerializer

    def get(self, request):
        sect = Sect.objects.all()

        response_data = []

        for sec in sect:
            response_data.append(sec.sector)

        return Response(response_data)