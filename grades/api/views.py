from rest_framework import viewsets, permissions
from ..models import Ocena, OcenaOkresowa, OcenaKoncowa, ZachowaniePunkty
from .serializers import (
    OcenaSerializer,
    OcenaOkresowaSerializer,
    OcenaKoncowaSerializer,
    ZachowaniePunktySerializer,
)
from authentication.api.permissions import IsAdminKeyAuthenticated


class OcenaViewSet(viewsets.ModelViewSet):
    queryset = Ocena.objects.all()
    serializer_class = OcenaSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Support filtering by uczen id using 'uczen' or 'user_id' for backward compatibility
        uczen_id = (
            self.request.query_params.get("uczen")
            or self.request.query_params.get("uczen_id")
            or self.request.query_params.get("user_id")
        )
        if uczen_id:
            queryset = queryset.filter(uczen_id=uczen_id)
        return queryset


class OcenaOkresowaViewSet(viewsets.ModelViewSet):
    queryset = OcenaOkresowa.objects.all()
    serializer_class = OcenaOkresowaSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        uczen_id = (
            self.request.query_params.get("uczen")
            or self.request.query_params.get("uczen_id")
            or self.request.query_params.get("user_id")
        )
        if uczen_id:
            queryset = queryset.filter(uczen_id=uczen_id)
        return queryset


class OcenaKoncowaViewSet(viewsets.ModelViewSet):
    queryset = OcenaKoncowa.objects.all()
    serializer_class = OcenaKoncowaSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        uczen_id = (
            self.request.query_params.get("uczen")
            or self.request.query_params.get("uczen_id")
            or self.request.query_params.get("user_id")
        )
        if uczen_id:
            queryset = queryset.filter(uczen_id=uczen_id)
        return queryset


class ZachowaniePunktyViewSet(viewsets.ModelViewSet):
    queryset = ZachowaniePunkty.objects.all()
    serializer_class = ZachowaniePunktySerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        uczen_id = (
            self.request.query_params.get("uczen")
            or self.request.query_params.get("uczen_id")
            or self.request.query_params.get("user_id")
        )
        if uczen_id:
            queryset = queryset.filter(uczen_id=uczen_id)
        return queryset
