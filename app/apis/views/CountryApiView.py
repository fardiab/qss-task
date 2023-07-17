from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response


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
