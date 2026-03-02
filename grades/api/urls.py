from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    OcenaViewSet,
    OcenaOkresowaViewSet,
    OcenaKoncowaViewSet,
    ZachowaniePunktyViewSet,
)

router = DefaultRouter()
router.register(r"oceny", OcenaViewSet)
router.register(r"oceny-okresowe", OcenaOkresowaViewSet)
router.register(r"oceny-koncowe", OcenaKoncowaViewSet)
router.register(r"zachowanie-punkty", ZachowaniePunktyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
