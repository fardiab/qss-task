from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter


class CountryApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        indicator = request.GET.get("indicator")
        queryset = (
            Country.objects.filter(indicator__indicator=indicator)
            .order_by("country")
            .values_list("country", flat=True)
            .distinct()
        )

        response_data = [{"subsector": subsector} for subsector in queryset]

        combined_response = {}
        for data in response_data:
            subsector_name = data["subsector"]
            combined_response[subsector_name] = subsector_name

        return Response(combined_response.values())
