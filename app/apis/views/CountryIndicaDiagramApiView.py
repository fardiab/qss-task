from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country, Indica
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max


class CountryIndicaDiagramApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        sector = request.GET.get("sector")
        subsector = request.GET.get("subsector")
        indicator = request.GET.getlist("indicator")

        indicators = (Country.objects.filter(
            country=selected_country,
            indicator__subsector__sector__sector=sector,
            indicator__subsector__subsector=subsector)
            .prefetch_related("indicator__subsector__sector")
            .values("indicator__indicator", "year", "rank", "indicator__subsector__sector__sector")
        )

        sector_rank_dict = defaultdict(list)

        for data in indicators:
            sector = data["indicator__subsector__sector__sector"]
            year = data["year"]
            rank = data["rank"]
            sector_rank_dict[sector].append(rank)

        max_rank_dict = {}

        for sector, ranks in sector_rank_dict.items():
            max_rank_sector = max(ranks)
            max_rank_dict[sector] = max_rank_sector

        indicator_data = defaultdict(list)

        for data in indicators:
            rank = data["rank"]
            year = data["year"]
            indicator_name = data["indicator__indicator"]
            max_rank = max_rank_dict[sector]
            score = round((1 - rank/ max_rank) * 100, 2)

            indicator_info = {
                "year": year,
                "score": score,
            }

            indicator_data[indicator_name].append(indicator_info)

        response_data = [{"indicator": key, "data": value} for key, value in indicator_data.items()]
        
        return Response(response_data)


        
