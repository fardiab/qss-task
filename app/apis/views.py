from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Sect, SubSect, Indica, Country
from .serializers import (
    SectSerializer,
    SubSectSerializer,
    IndicaSerializer,
    CountrySerializer,
)


class SectViewSet(viewsets.ModelViewSet):
    serializer_class = SectSerializer

    def get_queryset(self):
        queryset = Sect.objects.all()
        return queryset


class SubSectApiView(APIView):
    serializer_class = SubSectSerializer

    def get(self, request, pk=None):
        subsector = SubSect.objects.all()
        serializer = SubSectSerializer(subsector, many=True)
        return Response(serializer.data)


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


class CountryApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        count = int(request.GET.get("count", 0))
        selected_country = request.GET.getlist("country")
        year = request.GET.get("year", None)

        queryset = Country.objects.all()

        if selected_country:
            queryset = Country.objects.filter(country__in=selected_country)

        if year:
            queryset = queryset.filter(year=year)

        if count:
            queryset = queryset.order_by("-id")[:count]

        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)
