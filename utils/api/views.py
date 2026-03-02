from rest_framework import viewsets, permissions
from ..models import Przedmiot, Temat, PracaDomowa, DataSource
from .serializers import (
    PrzedmiotSerializer,
    TematSerializer,
    PracaDomowaSerializer,
    DataSourceSerializer,
)
from authentication.api.permissions import IsAdminKeyAuthenticated


class PrzedmiotViewSet(viewsets.ModelViewSet):
    queryset = Przedmiot.objects.all()
    serializer_class = PrzedmiotSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class TematViewSet(viewsets.ModelViewSet):
    queryset = Temat.objects.all()
    serializer_class = TematSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class PracaDomowaViewSet(viewsets.ModelViewSet):
    queryset = PracaDomowa.objects.all().order_by("-data_wystawienia")
    serializer_class = PracaDomowaSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        klasa_id = self.request.query_params.get("klasa_id")
        przedmiot_id = self.request.query_params.get("przedmiot_id")
        nauczyciel_id = self.request.query_params.get("nauczyciel_id")

        if klasa_id:
            queryset = queryset.filter(klasa_id=klasa_id)
        if przedmiot_id:
            queryset = queryset.filter(przedmiot_id=przedmiot_id)
        if nauczyciel_id:
            queryset = queryset.filter(nauczyciel_id=nauczyciel_id)
        return queryset


class DataSourceViewSet(viewsets.ModelViewSet):
    """
    Usually a singleton resource (pk=1).
    """

    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]
