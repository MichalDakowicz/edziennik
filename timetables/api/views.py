from rest_framework import viewsets, permissions
from ..models import (
    PlanyZajec,
    GodzinyLekcyjne,
    DniTygodnia,
    Zajecia,
    PlanWpis,
    Wydarzenie,
)
from .serializers import (
    PlanyZajecSerializer,
    GodzinyLekcyjneSerializer,
    DniTygodniaSerializer,
    ZajeciaSerializer,
    PlanWpisSerializer,
    WydarzenieSerializer,
)
from authentication.api.permissions import IsAdminKeyAuthenticated


class PlanyZajecViewSet(viewsets.ModelViewSet):
    queryset = PlanyZajec.objects.all()
    serializer_class = PlanyZajecSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class GodzinyLekcyjneViewSet(viewsets.ModelViewSet):
    queryset = GodzinyLekcyjne.objects.all()
    serializer_class = GodzinyLekcyjneSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class DniTygodniaViewSet(viewsets.ModelViewSet):
    queryset = DniTygodnia.objects.all().order_by("Numer")
    serializer_class = DniTygodniaSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class ZajeciaViewSet(viewsets.ModelViewSet):
    queryset = Zajecia.objects.all()
    serializer_class = ZajeciaSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class PlanWpisViewSet(viewsets.ModelViewSet):
    queryset = PlanWpis.objects.all()
    serializer_class = PlanWpisSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class WydarzenieViewSet(viewsets.ModelViewSet):
    queryset = Wydarzenie.objects.all()
    serializer_class = WydarzenieSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]
