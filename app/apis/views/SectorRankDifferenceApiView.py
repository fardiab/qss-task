from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter


class SectorRankDifferenceApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")
        year1 = request.GET.get("year1")
        year2 = request.GET.get("year2")
        sector = request.GET.get("sector")

        indicators1 = (
            Country.objects.filter(country=country, year=year1)
            .prefetch_related("indicator__subsector__sector")
            .select_related("indicator")
        )
        indicators2 = (
            Country.objects.filter(country=country, year=year2)
            .prefetch_related("indicator__subsector__sector")
            .select_related("indicator")
        )

        sector_rank_dict = defaultdict(list)
        for indicator1, indicator2 in zip(indicators1, indicators2):
            sector_rank_dict[indicator1.indicator.subsector.sector.sector].append(
                indicator1.rank - indicator2.rank
            )

        response_data = []
        for sector, rank_diffs in sector_rank_dict.items():
            if rank_diffs:
                rank_diff = sum(rank_diffs) / len(rank_diffs)
                rank_diff = round(rank_diff, 2)
                sector_info = {
                    "sector": sector,
                    "rank_difference": rank_diff,
                }
                response_data.append(sector_info)

        response_data.sort(key=itemgetter("sector"))

        return Response(response_data)
