from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country, Indica
from apis.serializers import CountrySerializer
from rest_framework.response import Response


class CountryIndicaRankDifferenceApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        year1 = request.GET.get("year1")
        year2 = request.GET.get("year2")
        sector = request.GET.get("sector")
        subsector = request.GET.get("subsector")

        indicators = Indica.objects.filter(
            subsector__subsector=subsector, subsector__sector__sector=sector
        ).values_list("indicator", flat=True)

        queryset1 = Country.objects.filter(
            indicator__subsector__sector__sector=sector,
            indicator__subsector__subsector=subsector,
            country=selected_country,
            year=year1,
        ).prefetch_related("indicator")

        queryset2 = Country.objects.filter(
            indicator__subsector__sector__sector=sector,
            indicator__subsector__subsector=subsector,
            country=selected_country,
            year=year2,
        ).prefetch_related("indicator")

        max_rank_dict1 = defaultdict(list)
        max_rank_dict2 = defaultdict(list)

        indicator_rank_dict1 = defaultdict(list)
        for data in queryset1:
            indicator = data.indicator.indicator
            rank = data.rank
            indicator_rank_dict1[indicator].append(rank)

        for indicator, ranks in indicator_rank_dict1.items():
            max_rank_indicator1 = max(ranks)
            max_rank_dict1[indicator] = max_rank_indicator1

        indicator_rank_dict2 = defaultdict(list)
        for data in queryset2:
            indicator = data.indicator.indicator
            rank = data.rank
            indicator_rank_dict2[indicator].append(rank)
        
        for indicator, ranks in indicator_rank_dict2.items():
            max_rank_indicator2 = max(ranks)
            max_rank_dict2[indicator] = max_rank_indicator2

        indicator_score_diff = defaultdict(list)

        for indicator, ranks in indicator_rank_dict1.items():
            total_score1 = 0
            total_score2 = 0
            num_sectors1 = 0
            num_sectors2 = 0

            for rank in ranks:
                total_score1 += rank
                num_sectors1 += 1

            for rank in indicator_rank_dict2[indicator]:
                total_score2 += rank
                num_sectors2 += 1

            avg_score1 = total_score1 / num_sectors1
            avg_score2 = total_score2 / num_sectors2

            score_diff = avg_score2 - avg_score1
            indicator_score_diff[indicator].append(score_diff)

        indicator_score_diff = dict(indicator_score_diff)

        for indicator, score_diff in indicator_score_diff.items():
            indicator_score_diff[indicator] = score_diff[0]

        sorted_indicator_score_diff = sorted(
            indicator_score_diff.items(), key=lambda x: x[1], reverse=True
        )

        return Response(sorted_indicator_score_diff)