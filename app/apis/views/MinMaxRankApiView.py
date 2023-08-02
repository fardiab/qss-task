from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from rest_framework.response import Response


class MinMaxRankApiView(APIView):
    def get(self, request):
        indicator = request.GET.get('indicator')
        year = request.GET.get('year')

        queryset = (Country.objects.filter(
            year=year, indicator__indicator=indicator
        ).order_by('rank')
        .values('rank'))

        min_rank = queryset.first()
        max_rank = queryset.last()

        return Response(max_rank)
