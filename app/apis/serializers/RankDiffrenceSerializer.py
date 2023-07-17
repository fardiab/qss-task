from rest_framework import serializers
from core.models import Country


class RankDiffrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("country", "rank", "year")
