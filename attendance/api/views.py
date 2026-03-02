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
        uczen_id = self.request.query_params.get("uczen_id")
        date = self.request.query_params.get("date")

        if uczen_id:
            queryset = queryset.filter(uczen_id=uczen_id)
        if date:
            queryset = queryset.filter(Data=date)
        return queryset
