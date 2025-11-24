from django.urls import path
from .views import (
    GodzinyLekcyjneApiView,
    DniTygodniaApiView,
    ZajeciaApiView,
    PlanWpisApiView,
    PlanyZajecApiView,
    WydarzenieApiView,
)

urlpatterns = [
    path("godziny-lekcyjne/", GodzinyLekcyjneApiView.as_view(), name="godziny-list"),
    path("godziny-lekcyjne/<int:pk>/", GodzinyLekcyjneApiView.as_view(), name="godziny-detail"),

    path("dni-tygodnia/", DniTygodniaApiView.as_view(), name="dni-list"),
    path("dni-tygodnia/<int:pk>/", DniTygodniaApiView.as_view(), name="dni-detail"),

    path("zajecia/", ZajeciaApiView.as_view(), name="zajecia-list"),
    path("zajecia/<int:pk>/", ZajeciaApiView.as_view(), name="zajecia-detail"),

    path("plan-wpisy/", PlanWpisApiView.as_view(), name="planwpis-list"),
    path("plan-wpisy/<int:pk>/", PlanWpisApiView.as_view(), name="planwpis-detail"),

    path("plany-zajec/", PlanyZajecApiView.as_view(), name="plany-list"),
    path("plany-zajec/<int:pk>/", PlanyZajecApiView.as_view(), name="plany-detail"),
    
    path("wydarzenia/", WydarzenieApiView.as_view(), name="wydarzenia-list"),
    path("wydarzenia/<int:pk>/", WydarzenieApiView.as_view(), name="wydarzenia-detail"),
]
