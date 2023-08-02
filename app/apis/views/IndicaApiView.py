from rest_framework.views import APIView
from core.models import Sect, SubSect
from apis.serializers import IndicaSerializer
from rest_framework.response import Response


class IndicaApiView(APIView):
    serializer_class = IndicaSerializer

    def get(self, request, pk=None):
        sector_name = request.query_params.get("sector")
        subsector_name = request.query_params.get("subsector")

        if pk is not None:
            try:
                sector = Sect.objects.prefetch_related("subsect_set__indica_set").get(
                    pk=pk
                )
                indicators_data = []

                for subsector in sector.subsect_set.all():
                    if subsector_name and subsector.subsector != subsector_name:
                        continue

                    indicators = subsector.indica_set.all()
                    indicator_data = [
                        {"indicator": indicator.indicator} for indicator in indicators
                    ]
                    indicators_data.extend(indicator_data)

                if subsector_name and not indicators_data:
                    return Response({"error": "Subsector not found"}, status=404)

                combined_response = {}
                for data in indicators_data:
                    indicator_name = data["indicator"]
                    combined_response[indicator_name] = indicator_name

                return Response(combined_response.values())

            except Sect.DoesNotExist:
                return Response({"error": "Sector not found"}, status=404)

        else:
            subsectors = SubSect.objects.filter(subsector=subsector_name)

            indicators_data = []

            for subsector in subsectors:
                if subsector_name and subsector.subsector != subsector_name:
                    continue

                indicators = subsector.indica_set.all()
                indicator_data = [
                    {"indicator": indicator.indicator} for indicator in indicators
                ]
                indicators_data.extend(indicator_data)

            if subsector_name and not indicators_data:
                return Response({"error": "Subsector not found"}, status=404)

            combined_response = {}
            for data in indicators_data:
                indicator_name = data["indicator"]
                combined_response[indicator_name] = indicator_name

            return Response(combined_response.values())
