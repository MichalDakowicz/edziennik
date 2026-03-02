from rest_framework import serializers
from ..models import StatusyObecnosci, Frekwencja


class StatusyObecnosciSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusyObecnosci
        fields = ["id", "Wartosc"]


class FrekwencjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frekwencja
        fields = ["id", "Data", "uczen", "godzina_lekcyjna", "status"]

    # Optional: If you want to accept 'uczen_id' in input but display as 'uczen',
    # default behavior of ModelSerializer handles this naturally (input: pk, output: pk).
    # The previous API used 'uczen_id' as key names. DRF uses 'uczen' by default.
    # To maintain strict compatibility with old field names if necessary:
    # uczen_id = serializers.PrimaryKeyRelatedField(queryset=Uczen.objects.all(), source='uczen', write_only=True)
    # But usually standardizing on field names is better.
    # Let's stick to DRF defaults for simplicity and "easly usable" request unless user needs strict backward comp.
    # Actually, the user wants "fully usable outside and easly usable", so standard DRF names (field names) are better.
