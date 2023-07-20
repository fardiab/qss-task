from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response


class CountryApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        queryset = (
            Country.objects.all()
            .values_list("indicator__subsector__subsector", flat=True)
            .distinct()
        )

        response_data = [{"subsector": subsector} for subsector in queryset]

        combined_response = {}
        for data in response_data:
            subsector_name = data["subsector"]
            combined_response[subsector_name] = subsector_name

        return Response(combined_response.values())
