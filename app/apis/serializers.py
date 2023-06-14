from rest_framework import serializers

from core.models import Sect, SubSect, Indica, CountryRank


class SectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sect
        fields = '__all__'


class SubSectSerializer(serializers.ModelSerializer):
    sector = serializers.StringRelatedField()

    class Meta:
        model = SubSect
        fields = '__all__'


class IndicaSerializer(serializers.ModelSerializer):
    subsector = serializers.StringRelatedField()
    
    class Meta:
        model = Indica
        exclude = ('description',)

class CountryRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryRank
        fields = '__all__'