from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F, IntegerField, ExpressionWrapper
from django.db.models.functions import Cast
from core.models import Sect, SubSect, Indica, Country
from .serializers import (
    SectSerializer,
    SubSectSerializer,
    IndicaSerializer,
    CountrySerializer,
    RankDiffrenceSerializer,
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
        indicator = request.GET.getlist("indicator", None)

        queryset = Country.objects.all()

        if indicator:
            queryset = queryset.filter(indicator__indicator__in=indicator)

        if selected_country:
            queryset = queryset.filter(country__in=selected_country)

        if year:
            queryset = queryset.filter(year=year)

        if count:
            queryset = queryset.order_by("-id")[:count]

        if not queryset.exists():
            return Response({"error": "No data found"}, status=404)

        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)


class RankDifferenceApiView(APIView):
    serializer_class = RankDiffrenceSerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        indicator = request.GET.get("indicator")
        year1 = request.GET.get("year1")
        year2 = request.GET.get("year2")

        queryset1 = Country.objects.filter(indicator__indicator=indicator, country=selected_country, year=year1)
        queryset2 = Country.objects.filter(indicator__indicator=indicator, country=selected_country, year=year2)

        rank_diff = None
        if queryset1.exists() and queryset2.exists():
            rank_diff1 = queryset1.first().rank
            rank_diff2 = queryset2.first().rank
            rank_diff = rank_diff1 - rank_diff2

        if rank_diff is None:
            return Response({"error": "No data found"}, status=404)

        return Response({
            "country": selected_country,
            "year1": year1,
            "year2" : year2,
            "rank_difference": rank_diff,
            })

        

        