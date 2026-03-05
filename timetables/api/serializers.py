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

    def validate(self, data):
        calodobowe = data.get("calodobowe", getattr(self.instance, "calodobowe", True))
        godzina_od = data.get("godzina_od", getattr(self.instance, "godzina_od", None))
        godzina_do = data.get("godzina_do", getattr(self.instance, "godzina_do", None))

        if not calodobowe:
            if godzina_od is None:
                raise serializers.ValidationError(
                    {
                        "godzina_od": "To pole jest wymagane gdy wydarzenie nie jest całodobowe."
                    }
                )
            if godzina_do is None:
                raise serializers.ValidationError(
                    {
                        "godzina_do": "To pole jest wymagane gdy wydarzenie nie jest całodobowe."
                    }
                )
            if godzina_od >= godzina_do:
                raise serializers.ValidationError(
                    {
                        "godzina_do": "Godzina zakończenia musi być późniejsza niż godzina rozpoczęcia."
                    }
                )
        return data
