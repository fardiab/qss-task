from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import RankDiffrenceSerializer
from rest_framework.response import Response


class RankDifferenceApiView(APIView):
    def get(self, request):
        countries = request.GET.getlist("country")
        indicator = request.GET.get("indicator")
        year1 = request.GET.get("year1")
        year2 = request.GET.get("year2")
        sector = request.GET.get("sector")
        subsector = request.GET.get("subsector")

        # Get data for year1
        queryset1 = Country.objects.filter(
            country__in=countries,
            indicator__indicator=indicator,
            # indicator__subsector__sector__sector=sector,
            # indicator__subsector__subsector=subsector,
            year=year1,
        ).values("country", "rank")

        # Get data for year2
        queryset2 = Country.objects.filter(
            country__in=countries,
            indicator__indicator=indicator,
            # indicator__subsector__sector__sector=sector,
            # indicator__subsector__subsector=subsector,
            year=year2,
        ).values("country", "rank")

        # Create a dictionary to store rank data for year1
        rank_by_country_year1 = {entry["country"]: entry["rank"] for entry in queryset1}

        # Create a dictionary to store rank data for year2
        rank_by_country_year2 = {entry["country"]: entry["rank"] for entry in queryset2}

        # Create a dictionary to store rank difference
        rank_diff_by_country = defaultdict(dict)

        for country in countries:
            # Check if the country has rank data for both years
            if country in rank_by_country_year1 and country in rank_by_country_year2:
                rank_diff_by_country[country] = {
                    "year1": rank_by_country_year1[country],
                    "year2": rank_by_country_year2[country],
                    "difference": rank_by_country_year1[country]
                    - rank_by_country_year2[country],
                }

        return Response(rank_diff_by_country)
