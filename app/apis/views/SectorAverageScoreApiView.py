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

        sector_data = {}
        for data in queryset:
            indicator = data["indicator__indicator"]
            rank = data["rank"]
            sector = data["indicator__subsector__sector__sector"]
            max_rank = max_rank_dict[sector]
            if rank == 0:
                continue
            score = round((1 - rank / max_rank) * 100, 2)
            if score == 0:
                continue
            if sector not in sector_data:
                sector_data[sector] = {"indicators": [], "total_score": 0, "count": 0}
            sector_data[sector]["indicators"].append(
                {
                    "indicator": indicator,
                    "score": score,
                }
            )
            sector_data[sector]["total_score"] += score
            sector_data[sector]["count"] += 1

        sector_info = []
        sc = 0
        for sector, data in sector_data.items():
            average_score = round(data["total_score"] / data["count"], 2)
            sc += average_score
            
        sc = round(sc/len(sector_data), 2)
        sector_info.append({
            "country": country,
            "average_score": sc,
        })

        return Response(sector_info)
