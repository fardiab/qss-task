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
        year1 = request.GET.get("year1")  # First year
        year2 = request.GET.get("year2")  # Second year

        indicators_data1 = (
            Country.objects.filter(country=country, year=year1)
            .prefetch_related("indicator__subsector__sector")
            .values("year", "indicator__subsector__sector__sector", "rank")
        )

        indicators_data2 = (
            Country.objects.filter(country=country, year=year2)
            .prefetch_related("indicator__subsector__sector")
            .values("year", "indicator__subsector__sector__sector", "rank")
        )

        max_rank_dict1 = defaultdict(list)
        max_rank_dict2 = defaultdict(list)

        sector_rank_dict1 = defaultdict(list)
        for data in indicators_data1:
            sector = data["indicator__subsector__sector__sector"]
            rank = data["rank"]
            sector_rank_dict1[sector].append(rank)

        for sector, ranks in sector_rank_dict1.items():
            max_rank_sector1 = max(ranks)
            max_rank_dict1[sector] = max_rank_sector1

        sector_rank_dict2 = defaultdict(list)
        for data in indicators_data2:
            sector = data["indicator__subsector__sector__sector"]
            rank = data["rank"]
            sector_rank_dict2[sector].append(rank)

        for sector, ranks in sector_rank_dict2.items():
            max_rank_sector2 = max(ranks)
            max_rank_dict2[sector] = max_rank_sector2

        sector_score_diff = {}

        for sector, ranks in sector_rank_dict1.items():
            total_score1 = 0
            total_score2 = 0
            num_sectors1 = 0
            num_sectors2 = 0

            for rank in ranks:
                max_rank_year1 = max_rank_dict1[sector]
                score1 = round((1 - rank / max_rank_year1) * 100, 2)
                if score1 == 0:
                    continue
                total_score1 += score1
                num_sectors1 += 1

            if sector in sector_rank_dict2:
                for rank in sector_rank_dict2[sector]:
                    max_rank_year2 = max_rank_dict2[sector]
                    score2 = round((1 - rank / max_rank_year2) * 100, 2)
                    if score2 == 0:
                        continue
                    total_score2 += score2
                    num_sectors2 += 1

            # Calculate average scores for both years
            if num_sectors1 != 0:
                average_score1 = round(total_score1 / num_sectors1, 2)
            if num_sectors2 != 0:
                average_score2 = round(total_score2 / num_sectors2, 2) if num_sectors2 > 0 else None

            # Calculate score difference
            score_difference = (
                round(average_score2 - average_score1, 2) if average_score2 is not None else None
            )

            sector_score_diff[sector] = score_difference
        
        sector_score_diff = sorted(sector_score_diff.items(), key=itemgetter(0))

        return Response(sector_score_diff)