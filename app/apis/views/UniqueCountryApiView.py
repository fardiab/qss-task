from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter
import pandas as pd


class UniqueCountryApiView(APIView):
    # serializer_class = CountrySerializer

    def get(self, request):
        countries = Country.objects.values_list("country", flat=True).distinct()

        # data.sort(key=itemgetter('countries'))

        return Response(sorted(countries))
