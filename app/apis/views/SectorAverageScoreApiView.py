from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter


class SectorAverageScoreApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")
        year = request.GET.get("year")
        sector = request.GET.get("sector")
        queryset = Country.objects.filter(country=country, year=year).values(
            "indicator__indicator", "rank", "indicator__subsector__sector__sector"
        )
        indicators = (
            Country.objects.filter(country=country, year=year)
            .prefetch_related("indicator__subsector__sector")
            .values_list("rank", "indicator__subsector__sector__sector")
        )

        sector_rank_dict = defaultdict(list)
        for rank, sector in indicators:
            sector_rank_dict[sector].append(rank)
        max_rank_dict = {}
        for sector, ranks in sector_rank_dict.items():
            max_rank_sector = max(ranks)
            max_rank_dict[sector] = max_rank_sector

        total_score = 0
        num_sectors = 0

        for rank, sector in indicators:
            max_rank = max_rank_dict[sector]
            if rank == 0:
                continue
            score = round((1 - rank / max_rank) * 100, 2)
            if score == 0:
                continue
            total_score += score
            num_sectors += 1
        if num_sectors == 0:
            average_score = 0
        else:
            average_score = round(total_score / num_sectors, 2)

        return Response({"country": country, "average_score": average_score})
