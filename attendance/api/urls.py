from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StatusyObecnosciViewSet, FrekwencjaViewSet

router = DefaultRouter()
router.register(r"statusy", StatusyObecnosciViewSet)
router.register(r"frekwencja", FrekwencjaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
