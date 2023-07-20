from rest_framework.views import APIView
from core.models import SubSect
from apis.serializers import SubSectSerializer
from rest_framework.response import Response


class SubSectApiView(APIView):
    serializer_class = SubSectSerializer

    def get(self, request, pk=None):
        sector = request.GET.get("sector")
        subsector = SubSect.objects.filter(sector__sector=sector)

        response_data = []

        for subsect in subsector:
            response_data.append(subsect.subsector)

        return Response(response_data)
