from rest_framework.views import APIView
from core.models import Country
from apis.serializers import RankDiffrenceSerializer
from rest_framework.response import Response


class RankDifferenceApiView(APIView):
    serializer_class = RankDiffrenceSerializer

    def get(self, request):
        selected_countries = request.GET.getlist("country")
        indicator = request.GET.get("indicator")
        year1 = request.GET.get("year1")
        year2 = request.GET.get("year2")

        rank_diff_by_country = {}

        queryset1 = Country.objects.filter(
            indicator__indicator=indicator, year=year1, country__in=selected_countries
        ).values("country", "rank")

        queryset2 = Country.objects.filter(
            indicator__indicator=indicator, year=year2, country__in=selected_countries
        ).values("country", "rank")

        for data1, data2 in zip(queryset1, queryset2):
            country = data1["country"]
            rank1 = data1["rank"]
            rank2 = data2["rank"]

            rank_diff = rank1 - rank2

            if country not in rank_diff_by_country:
                rank_diff_by_country[country] = rank_diff

        rank_diff_response = {
            "year1": year1,
            "year2": year2,
            "rank_diff": rank_diff_by_country,
        }

        return Response(rank_diff_response)
