from rest_framework import serializers

from core.models import Sect, SubSect, Indica, Country


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

class CountrySerializer(serializers.ModelSerializer):
    indicator = serializers.StringRelatedField()

    class Meta:
        model = Country
        fields = '__all__'