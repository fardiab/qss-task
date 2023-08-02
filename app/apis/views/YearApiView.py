from rest_framework.views import APIView
from core.models import Country
from rest_framework.response import Response


class YearApiView(APIView):
    def get(self, request):
        countries = str(request.GET.get("country")).split(",")
        indicator = request.GET.get("indicator")

        queryset = (
            Country.objects.filter(country__in=countries, indicator__indicator=indicator)
            .order_by("year")
            .values_list("year", flat=True)
            .distinct()
        )

        response_data = [{"year": year} for year in queryset]

        combined_response = {}
        for data in response_data:
            year = data["year"]
            combined_response[year] = year

        # print(len(combined_response))

        return Response(combined_response.values())