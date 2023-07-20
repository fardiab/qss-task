from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max, Subquery, OuterRef


class SectorYearScoreApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        sector = request.GET.get("sector")
        country = request.GET.get("country")

        max_rank_subquery = (
            Country.objects.filter(
                indicator__indicator=OuterRef("indicator__indicator"),
                indicator__subsector__sector__sector=sector,
                country=country,
            )
            .values("indicator__indicator")
            .annotate(max_rank=Max("rank"))
            .values("max_rank")
        )

        queryset = (
            Country.objects.filter(
                indicator__subsector__sector__sector=sector, country=country
            )
            .annotate(max_rank=Subquery(max_rank_subquery))
            .values("rank", "indicator__subsector__sector__sector", "max_rank", "year")
            .prefetch_related("indicator")
        )

        sector_data = {}
        for data in queryset:
            rank = data["rank"]
            max_rank = data["max_rank"]
            year = data["year"]

            if rank == 0:
                continue

            score = round((1 - rank / max_rank) * 100, 2)

            if score == 0:
                continue

            if year not in sector_data:
                sector_data[year] = score
            elif score > sector_data[year]:
                sector_data[year] = score

        result = [{"year": year, "score": score} for year, score in sector_data.items()]

        return Response(result)
