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

        indicators = (
            Country.objects.filter(country=country)
            .prefetch_related("indicator__subsector__sector")
            .values_list("year", "rank", "indicator__subsector__sector__sector")
        )

        year_rank_dict = defaultdict(dict)
        for year, rank, sector in indicators:
            if sector in year_rank_dict[year]:
                year_rank_dict[year][sector].append(rank)
            else:
                year_rank_dict[year][sector] = [rank]

        response_data = []
        for year, sector_ranks in year_rank_dict.items():
            year_scores = []
            for sector, ranks in sector_ranks.items():
                max_rank_sector = max(ranks)
                if ranks:
                    rank = sum(ranks) / len(ranks)
                    rank = round(rank, 2)
                    score = round((1 - rank / max_rank_sector) * 100, 2)
                    sector_info = {
                        "year": year,
                        "sector": sector,
                        "score": score,
                    }
                    year_scores.append(sector_info)

            response_data.extend(year_scores)

        # response_data = sorted(response_data, key=itemgetter('year'))
        response_data = sorted(response_data, key=itemgetter("sector"))

        return Response(response_data)
