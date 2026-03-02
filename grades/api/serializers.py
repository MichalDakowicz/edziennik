from rest_framework import serializers
from ..models import Ocena, OcenaOkresowa, OcenaKoncowa, ZachowaniePunkty


class OcenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocena
        fields = "__all__"


class OcenaOkresowaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcenaOkresowa
        fields = "__all__"


class OcenaKoncowaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcenaKoncowa
        fields = "__all__"


class ZachowaniePunktySerializer(serializers.ModelSerializer):
    class Meta:
        model = ZachowaniePunkty
        fields = "__all__"
