from rest_framework.views import APIView
from core.models import SubSect
from apis.serializers import SubSectSerializer
from rest_framework.response import Response


class SubSectApiView(APIView):
    serializer_class = SubSectSerializer

    def get(self, request, pk=None):
        subsector = SubSect.objects.all()
        serializer = SubSectSerializer(subsector, many=True)
        return Response(serializer.data)
