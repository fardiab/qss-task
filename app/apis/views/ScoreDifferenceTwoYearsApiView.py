from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter
from django.db.models import Avg, Max


class ScoreDifferenceTwoYearsApiView(APIView):
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

        max_rank_dict1 = {}
        max_rank_dict2 = {}

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

        total_score1 = 0
        total_score2 = 0
        num_sectors1 = 0
        num_sectors2 = 0

        for data in indicators_data1:
            rank = data["rank"]
            sector = data["indicator__subsector__sector__sector"]
            max_rank_year1 = max_rank_dict1[sector]
            score1 = round((1 - rank / max_rank_year1) * 100, 2)
            if score1 == 0:
                continue
            total_score1 += score1
            num_sectors1 += 1

        for data in indicators_data2:
            rank = data["rank"]
            sector = data["indicator__subsector__sector__sector"]
            max_rank_year2 = max_rank_dict2[sector]
            score2 = round((1 - rank / max_rank_year2) * 100, 2)
            if score2 == 0:
                continue
            total_score2 += score2
            num_sectors2 += 1
        
        # Calculate average scores for both years
        average_score1 = round(total_score1 / num_sectors1, 2)
        average_score2 = round(total_score2 / num_sectors2, 2)

        # Calculate score difference
        score_difference = round(average_score1 - average_score2, 2)

        response_data = {
            "country": country,
            "score_difference": score_difference,
        }

        return Response(response_data)

