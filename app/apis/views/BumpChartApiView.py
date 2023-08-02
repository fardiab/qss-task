from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from rest_framework.response import Response


class BumpChartApiView(APIView):
    def get(self, request):
        countries = request.GET.getlist("country")
        indicator = request.GET.get("indicator")
        sector = request.GET.get("sector")
        subsector = request.GET.get("subsector")

        queryset = Country.objects.filter(
            country__in=countries,
            indicator__indicator=indicator,
            indicator__subsector__sector__sector=sector,
            indicator__subsector__subsector=subsector,
        ).values("country", "rank", "year")

        response_data = defaultdict(dict)

        for entry in queryset:
            country = entry["country"]
            year = entry["year"]
            rank = entry["rank"]

            # Add country if not already in response_data
            if country not in response_data:
                response_data[country] = {}

            # Add year-rank data to the respective country
            response_data[country][year] = rank

        # Convert the nested dictionary to a list of dictionaries
        # containing "country" and its year-rank data
        response_list = [
            {"country": country, "rank_by_year": data}
            for country, data in response_data.items()
        ]

        count1 = int(request.GET.get("count1", 1))  # Default value is 1 if not provided
        count2 = int(request.GET.get("count2", len(response_list)))  # Default value is the total number of countries if not provided

        # Return the response data for the specified range of countries
        return Response(response_list[count1-1:count2])