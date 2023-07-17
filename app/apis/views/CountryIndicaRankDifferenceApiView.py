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

        indicator_rank_dict = {}
        for country1, country2 in zip(queryset1, queryset2):
            indicator_rank_dict[
                (country1.indicator.indicator, country1.year)
            ] = country1.rank
            indicator_rank_dict[
                (country2.indicator.indicator, country2.year)
            ] = country2.rank

        response_data = []
        for indicator in indicators:
            rank_diff = None
            rank1 = indicator_rank_dict.get((indicator, year1))
            rank2 = indicator_rank_dict.get((indicator, year2))
            if rank1 is not None and rank2 is not None:
                rank_diff = rank1 - rank2

            if rank_diff is None:
                continue

            indicator_info = {
                "indicator": indicator,
                "rank_diff": rank_diff,
            }

            response_data.append(indicator_info)

        return Response(response_data)
