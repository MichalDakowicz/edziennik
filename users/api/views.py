from rest_framework import viewsets, permissions
from ..models import Uczen, Nauczyciel, Rodzic, UserProfile, Klasa, Adres, Wiadomosc
from .serializers import (
    UczenSerializer,
    NauczycielSerializer,
    RodzicSerializer,
    UserProfileSerializer,
    KlasaSerializer,
    AdresSerializer,
    WiadomoscSerializer,
)
from authentication.api.permissions import IsAdminKeyAuthenticated


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
