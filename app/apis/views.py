from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F, IntegerField, ExpressionWrapper, Max
from django.core import serializers
import json
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
        selected_countries = request.GET.getlist("country")
        indicator = request.GET.get("indicator")
        year1 = request.GET.get("year1")
        year2 = request.GET.get("year2")

        rank_diff_by_country = {}

        for country in selected_countries:
            queryset1 = Country.objects.filter(
                indicator__indicator=indicator, country=country, year=year1
            )
            queryset2 = Country.objects.filter(
                indicator__indicator=indicator, country=country, year=year2
            )

            rank_diff = None
            if queryset1.exists() and queryset2.exists():
                rank_diff1 = queryset1.first().rank
                rank_diff2 = queryset2.first().rank
                rank_diff = rank_diff1 - rank_diff2

            if rank_diff is None:
                rank_diff = "No data found"

            rank_diff_by_country[country] = rank_diff

        return Response(
            {"year1": year1, "year2": year2, "rank_diff": rank_diff_by_country}
        )


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
                "sector": sector,
                "subsector": subsector,
                "indicator": data["indicator__indicator"],
                "score": score,
            }
            response_data.append(indicator_info)

        return Response(response_data)


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
            indicator_rank_dict[(country1.indicator.indicator, country1.year)] = country1.rank
            indicator_rank_dict[(country2.indicator.indicator, country2.year)] = country2.rank

        response_data = []
        for indicator in indicators:
            rank_diff = None
            rank1 = indicator_rank_dict.get((indicator, year1))
            rank2 = indicator_rank_dict.get((indicator, year2))
            if rank1 is not None and rank2 is not None:
                rank_diff = rank1 - rank2

            indicator_info = {
                "indicator": indicator,
                "rank_diff": rank_diff,
            }

            response_data.append(indicator_info)

        return Response(response_data)
