from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    PlanyZajecViewSet,
    GodzinyLekcyjneViewSet,
    DniTygodniaViewSet,
    ZajeciaViewSet,
    PlanWpisViewSet,
    WydarzenieViewSet,
)

router = DefaultRouter()
router.register(r"plany-zajec", PlanyZajecViewSet)
router.register(r"godziny-lekcyjne", GodzinyLekcyjneViewSet)
router.register(r"dni-tygodnia", DniTygodniaViewSet)
router.register(r"zajecia", ZajeciaViewSet)
router.register(r"plan-wpisy", PlanWpisViewSet)
router.register(r"wydarzenia", WydarzenieViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
