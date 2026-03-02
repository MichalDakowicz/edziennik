from rest_framework import serializers
from ..models import Przedmiot, Temat, PracaDomowa, DataSource


class PrzedmiotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Przedmiot
        fields = "__all__"


class TematSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temat
        fields = "__all__"


class PracaDomowaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracaDomowa
        fields = "__all__"


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = "__all__"
