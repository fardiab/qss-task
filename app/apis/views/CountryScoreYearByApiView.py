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

        indicators_data = (
            Country.objects.filter(country=country)
            .prefetch_related("indicator__subsector__sector")
            .values("year", "rank", "indicator__subsector__sector__sector")
        )

        year_rank_dict = defaultdict(list)
        for data in indicators_data:
            year = data["year"]
            rank = data["rank"]
            sector_name = data["indicator__subsector__sector__sector"]
            year_rank_dict[year].append(rank)

        response_data = []
        for year, ranks in year_rank_dict.items():
            max_rank_year = max(ranks)
            rank_sum = sum(ranks)
            average_rank = rank_sum / len(ranks)
            average_rank = round(average_rank, 2)
            score = round((1 - average_rank / max_rank_year) * 100, 2)
            year_info = {
                "year": year,
                "score": score,
            }
            response_data.append(year_info)

        response_data.sort(key=itemgetter("score"), reverse=True) 

        return Response(response_data)