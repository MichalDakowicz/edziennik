from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response

from ..models import Uczen, Nauczyciel, Rodzic, UserProfile, Klasa, Adres, Wiadomosc
from .serializers import (
    UczenSerializer,
    NauczycielSerializer,
    RodzicSerializer,
    UserProfileSerializer,
    UserDisplaySerializer,
    KlasaSerializer,
    AdresSerializer,
    WiadomoscSerializer,
)
from authentication.api.permissions import IsAdminKeyAuthenticated

User = get_user_model()


class UczenViewSet(viewsets.ModelViewSet):
    queryset = Uczen.objects.all()
    serializer_class = UczenSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class NauczycielViewSet(viewsets.ModelViewSet):
    queryset = Nauczyciel.objects.all()
    serializer_class = NauczycielSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class RodzicViewSet(viewsets.ModelViewSet):
    queryset = Rodzic.objects.all()
    serializer_class = RodzicSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Read-only lookup of user display info by user id (e.g. for message sender names).
    Only GET /users/<id>/ is allowed; list is disabled.
    """
    queryset = User.objects.all()
    serializer_class = UserDisplaySerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed."}, status=405)


class KlasaViewSet(viewsets.ModelViewSet):
    queryset = Klasa.objects.all()
    serializer_class = KlasaSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class AdresViewSet(viewsets.ModelViewSet):
    queryset = Adres.objects.all()
    serializer_class = AdresSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]


class WiadomoscViewSet(viewsets.ModelViewSet):
    queryset = Wiadomosc.objects.all()
    serializer_class = WiadomoscSerializer
    permission_classes = [permissions.IsAuthenticated | IsAdminKeyAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        odbiorca_id = self.request.query_params.get("odbiorca")
        if odbiorca_id:
            queryset = queryset.filter(odbiorca_id=odbiorca_id)
        return queryset
