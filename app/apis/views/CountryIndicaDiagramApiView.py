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
        indicator_names = request.GET.getlist("indicator")

        indicator_ids = Indica.objects.filter(
            indicator__in=indicator_names
        ).values_list("id", flat=True)

        queryset = Country.objects.filter(
            country=selected_country,
            indicator__id__in=indicator_ids,
            indicator__subsector__subsector=subsector,
            indicator__subsector__sector__sector=sector,
        ).values("indicator__indicator", "year", "rank")

        max_ranks = (
            Country.objects.filter(
                indicator__subsector__subsector=subsector,
                indicator__subsector__sector__sector=sector,
                indicator__id__in=indicator_ids,
            )
            .values("indicator__indicator")
            .annotate(max_rank=Max("rank"))
        )

        max_rank_dict = {
            item["indicator__indicator"]: item["max_rank"] for item in max_ranks
        }

        response_data = []
        for data in queryset:
            max_rank = max_rank_dict[data["indicator__indicator"]]
            score = round((1 - data["rank"] / max_rank) * 100, 2)

            indicator_info = {
                "indicator": data["indicator__indicator"],
                "year": data["year"],
                "score": score,
            }
            response_data.append(indicator_info)

        return Response(response_data)
