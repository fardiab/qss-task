from rest_framework import serializers
from core.models import Indica


class IndicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indica
        fields = "__all__"
