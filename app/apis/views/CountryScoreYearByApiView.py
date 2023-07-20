from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter


class CountryScoreYearByApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")
        sector = request.GET.get("sector")
        year = request.GET.get("year")

        indicators_data = (
            Country.objects.filter(
                country=country, indicator__subsector__sector__sector=sector
            )
            .prefetch_related("indicator__subsector__sector")
            .values(
                "year",
                "rank",
                "indicator__subsector__sector__sector",
                "indicator__indicator",
            )
        )

        if sector:
            indicators_data = [
                data
                for data in indicators_data
                if data["indicator__subsector__sector__sector"] == sector
            ]

        year_rank_dict = defaultdict(list)
        for data in indicators_data:
            rank = data["rank"]
            year = data["year"]
            year_rank_dict[year].append(rank)

        max_rank_dict = {}
        for year, ranks in year_rank_dict.items():
            max_rank_year = max(ranks)
            max_rank_dict[year] = max_rank_year

        response_data = []
        for year, ranks in year_rank_dict.items():
            max_rank_year = max_rank_dict[year]
            if ranks:
                rank_sum = sum(ranks)
                average_rank = rank_sum / len(ranks)
                average_rank = round(average_rank, 2)
                score = round((1 - average_rank / max_rank_year) * 100, 2)

                response_data.append(
                    {
                        "year": year,
                        "average_score": score,
                    }
                )

        response_data = sorted(response_data, key=itemgetter("year"))

        return Response(response_data)
