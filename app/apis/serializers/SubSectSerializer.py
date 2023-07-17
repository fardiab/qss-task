from rest_framework import serializers
from core.models import SubSect


class SubSectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSect
        fields = "__all__"
