from collections import defaultdict
from rest_framework.views import APIView
from core.models import Indica, Country
from rest_framework.response import Response


class DescriptionApiView(APIView):
    def get(self, request):
        sector = request.GET.get("sector")

        queryset = (
            Country.objects.filter(indicator__subsector__sector__sector=sector)
            .select_related("indicator__subsector__sector")
            .prefetch_related("indicator")
            .values(
                "indicator__subsector__subsector",
                "indicator__indicator",
                "indicator__content",
            )
            .distinct()
        )

        response_data = defaultdict(list)

        for data in queryset:
            subsector = data["indicator__subsector__subsector"]
            indicator = data["indicator__indicator"]
            content = data["indicator__content"]

            response_data[subsector].append(
                {
                    "indicator": indicator,
                    "content": content if content else "No description",
                }
            )

        return Response(response_data)
