from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from rest_framework.response import Response
from django.db.models import Q, Min, Max
from operator import itemgetter


class BarChartApiView(APIView):
    def get(self, request):
        countries = str(request.GET.get("country")).split(",")
        indicator = request.GET.get("indicator")
        sector = request.GET.get("sector")
        subsector = request.GET.get("subsector")
        year = request.GET.get("year")

        queryset = Country.objects.filter(
            country__in=countries,
            indicator__indicator=indicator,
            indicator__subsector__sector__sector=sector,
            indicator__subsector__subsector=subsector,
            year=year,
        ).values("country", "rank", "amount")

        q = Country.objects.filter(
            indicator__indicator=indicator,
            year=year,
        ).values("rank", "amount")

        queryset_rank = (Country.objects.filter(
            year=year, indicator__indicator=indicator
        ).order_by('rank')
        .values('rank'))

        min_rank = queryset_rank.first()
        max_rank = queryset_rank.last()

        print(min_rank.values(), max_rank.values())


        rank_by_country = {entry["country"]: entry["rank"] for entry in queryset}

        response_data = defaultdict(dict)

        count1 = int(request.GET.get("count1", 1)) 
        count2 = int(request.GET.get("count2", len(countries)))
        
        countries_to_show = countries[count1-1:count2]

        min_amount = q.all().aggregate(Min('amount'))['amount__min']
        max_amount = q.all().aggregate(Max('amount'))['amount__max']


        formula = lambda x: (float(x) - float(min_amount)) / (float(max_amount) - float(min_amount)) * 100



        for country in countries_to_show:
            if country in rank_by_country:
                response_data[country] = {
                    "country": country,
                    "rank": rank_by_country[country],
                    "amount": queryset.get(country=country)["amount"],
                    "percentage": round(formula(queryset.get(country=country)["amount"]), 1),
                    
                }

        # response_data = response_data.sort(key=itemgetter('percentage'), reverse=True)


        return Response(response_data)
