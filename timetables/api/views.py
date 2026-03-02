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

    def get_queryset(self):
        queryset = super().get_queryset()
        klasa_id = self.request.query_params.get("klasa_id")
        if klasa_id:
            queryset = queryset.filter(klasa_id=klasa_id)
        return queryset


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

    def get_queryset(self):
        queryset = super().get_queryset()
        plan_id = self.request.query_params.get("plan_id")
        if plan_id:
            # Filter wpisy that belong to a specific plan
            try:
                plan = PlanyZajec.objects.get(id=plan_id)
                return plan.wpisy.all()
            except PlanyZajec.DoesNotExist:
                return PlanWpis.objects.none()
        return queryset


class WydarzenieViewSet(viewsets.ModelViewSet):
    queryset = Wydarzenie.objects.all()
    serializer_class = WydarzenieSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]
