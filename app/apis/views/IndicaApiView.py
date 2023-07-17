from rest_framework.views import APIView
from core.models import Sect
from apis.serializers import IndicaSerializer
from rest_framework.response import Response


class IndicaApiView(APIView):
    serializer_class = IndicaSerializer

    def get(self, request, pk=None):
        if pk is not None:
            try:
                sector = Sect.objects.prefetch_related("subsect_set__indica_set").get(
                    pk=pk
                )
                data = []
                for subsector in sector.subsect_set.all():
                    indicators = subsector.indica_set.all()
                    indicator_data = [
                        {"id": indicator.id, "indicator": indicator.indicator}
                        for indicator in indicators
                    ]
                    data.append(
                        {
                            "id": subsector.id,
                            "subsector": subsector.subsector,
                            "indicators": indicator_data,
                        }
                    )
                sector_data = {
                    "id": sector.id,
                    "sector": sector.sector,
                    "subsectors": data,
                }
                return Response(sector_data)
            except Sect.DoesNotExist:
                return Response({"error": "Sector not found"}, status=404)
        else:
            sectors = Sect.objects.all()
            data = []
            for sector in sectors:
                subsector_data = []
                for subsector in sector.subsect_set.all():
                    indicators = subsector.indica_set.all()
                    indicator_data = [
                        {"id": indicator.id, "indicator": indicator.indicator}
                        for indicator in indicators
                    ]
                    subsector_data.append(
                        {
                            "id": subsector.id,
                            "subsector": subsector.subsector,
                            "indicators": indicator_data,
                        }
                    )
                sector_data = {
                    "id": sector.id,
                    "sector": sector.sector,
                    "subsectors": subsector_data,
                }
                data.append(sector_data)
            return Response(data)
