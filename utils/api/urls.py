from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .lucky_number import LuckyNumberView
from .views import (
    PrzedmiotViewSet,
    TematViewSet,
    PracaDomowaViewSet,
    DataSourceViewSet,
)

router = DefaultRouter()
router.register(r"przedmioty", PrzedmiotViewSet)
router.register(r"tematy", TematViewSet)
router.register(r"prace-domowe", PracaDomowaViewSet)
router.register(r"datasource", DataSourceViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lucky-number/", LuckyNumberView.as_view(), name="lucky-number"),
]
