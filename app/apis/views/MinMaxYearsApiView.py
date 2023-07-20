from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max
from operator import itemgetter


class MinMaxYearsApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        years = Country.objects.values_list("year", flat=True).distinct()

        min_year = min(years)
        max_year = max(years)

        response_data = {"min_year": min_year, "max_year": max_year}

        data = []
        data.append(response_data)

        return Response(response_data)
