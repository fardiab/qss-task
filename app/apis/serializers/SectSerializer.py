from rest_framework import serializers
from core.models import Sect


class SectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sect
        fields = "__all__"
