from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    UczenViewSet,
    NauczycielViewSet,
    RodzicViewSet,
    UserProfileViewSet,
    UserViewSet,
    KlasaViewSet,
    AdresViewSet,
    WiadomoscViewSet,
)

router = DefaultRouter()
router.register(r"uczniowie", UczenViewSet)
router.register(r"nauczyciele", NauczycielViewSet)
router.register(r"rodzice", RodzicViewSet)
router.register(r"profile", UserProfileViewSet)
router.register(r"users", UserViewSet)
router.register(r"klasy", KlasaViewSet)
router.register(r"adresy", AdresViewSet)
router.register(r"wiadomosci", WiadomoscViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
