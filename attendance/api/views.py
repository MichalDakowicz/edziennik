from rest_framework import viewsets, permissions
from ..models import StatusyObecnosci, Frekwencja
from .serializers import StatusyObecnosciSerializer, FrekwencjaSerializer
from authentication.api.permissions import IsAdminKeyAuthenticated


class StatusyObecnosciViewSet(viewsets.ModelViewSet):
    queryset = StatusyObecnosci.objects.all()
    serializer_class = StatusyObecnosciSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class FrekwencjaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows attendance records to be viewed or edited.
    Supports filtering by 'uczen_id' (student id) and 'date' (date string).
    """

    queryset = Frekwencja.objects.all()
    serializer_class = FrekwencjaSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        uczen_id = (
            self.request.query_params.get("uczen_id")
            or self.request.query_params.get("uczen")
        )
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if uczen_id:
            queryset = queryset.filter(uczen_id=uczen_id)
        if date_from:
            queryset = queryset.filter(Data__gte=date_from)
        if date_to:
            queryset = queryset.filter(Data__lte=date_to)
        return queryset
