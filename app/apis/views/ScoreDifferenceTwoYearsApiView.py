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

        indicators_1 = (
            Country.objects.filter(country=country, year=year1)
            .prefetch_related("indicator__subsector__sector")
            .values("indicator__subsector__sector__sector")
            .annotate(avg_rank1=Avg("rank"), max_rank1=Max("rank"))
        )

        indicators_2 = (
            Country.objects.filter(country=country, year=year2)
            .prefetch_related("indicator__subsector__sector")
            .values("indicator__subsector__sector__sector")
            .annotate(avg_rank2=Avg("rank"), max_rank2=Max("rank"))
        )

        sector_data = defaultdict(dict)
        for data in indicators_1:
            sector = data["indicator__subsector__sector__sector"]
            sector_data[sector]["avg_rank1"] = data["avg_rank1"]
            sector_data[sector]["max_rank1"] = data["max_rank1"]

        for data in indicators_2:
            sector = data["indicator__subsector__sector__sector"]
            sector_data[sector]["avg_rank2"] = data["avg_rank2"]
            sector_data[sector]["max_rank2"] = data["max_rank2"]

        response_data = []
        total_score1 = 0
        total_score2 = 0
        num_sectors1 = 0
        num_sectors2 = 0

        for sector, data in sector_data.items():
            avg_rank1 = data.get("avg_rank1", 0)
            max_rank1 = data.get("max_rank1", 0)
            avg_rank2 = data.get("avg_rank2", 0)
            max_rank2 = data.get("max_rank2", 0)

            if max_rank1 != 0:
                score1 = 1 - avg_rank1 / max_rank1
            else:
                score1 = 0.0

            if max_rank2 != 0:
                score2 = 1 - avg_rank2 / max_rank2
            else:
                score2 = 0.0

            # response_data.append({
            #     "sector": sector,
            #     "year1": year1,
            #     "score1": score1,
            #     "year2": year2,
            #     "score2": score2,
            # })

            total_score1 += score1
            total_score2 += score2
            num_sectors1 += 1
            num_sectors2 += 1

        # Calculate average scores
        if num_sectors1 > 0:
            average_score1 = round(total_score1 / num_sectors1, 2)
        else:
            average_score1 = 0.0

        if num_sectors2 > 0:
            average_score2 = round(total_score2 / num_sectors2, 2)
        else:
            average_score2 = 0.0

        # Calculate score difference
        score_difference = round(average_score1 - average_score2, 2)

        response_data.append(
            {
                "country": country,
                "score_difference": score_difference,
            }
        )

        return Response({"country": country, "score_difference": score_difference})
