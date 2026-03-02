from rest_framework import serializers
from ..models import (
    PlanyZajec,
    GodzinyLekcyjne,
    DniTygodnia,
    Zajecia,
    PlanWpis,
    Wydarzenie,
)


class GodzinyLekcyjneSerializer(serializers.ModelSerializer):
    class Meta:
        model = GodzinyLekcyjne
        fields = "__all__"


class DniTygodniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DniTygodnia
        fields = "__all__"


class ZajeciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zajecia
        fields = "__all__"


class PlanWpisSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanWpis
        fields = "__all__"


class PlanyZajecSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanyZajec
        fields = "__all__"


class WydarzenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wydarzenie
        fields = "__all__"
