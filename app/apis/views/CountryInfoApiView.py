from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max


class CountryInfoApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        year = request.GET.get("year")
        sector = request.GET.get("sector")
        subsector = request.GET.get("subsector")

        indicators_data = Country.objects.filter(
            country=selected_country,
            year=year,
            indicator__subsector__subsector=subsector,
            indicator__subsector__sector__sector=sector,
        ).values("indicator__indicator", "rank")

        max_ranks = (
            Country.objects.filter(
                year=year,
                indicator__subsector__subsector=subsector,
                indicator__subsector__sector__sector=sector,
            )
            .values("indicator__indicator")
            .annotate(max_rank=Max("rank"))
        )

        max_rank_dict = {
            item["indicator__indicator"]: item["max_rank"] for item in max_ranks
        }

        response_data = []
        for data in indicators_data:
            max_rank = max_rank_dict[data["indicator__indicator"]]
            score = round((1 - data["rank"] / max_rank) * 100, 2)

            indicator_info = {
                "indicator": data["indicator__indicator"],
                "score": score,
            }
            response_data.append(indicator_info)

        return Response(sorted(response_data,lambda x:x['score']) )
