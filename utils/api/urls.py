from django.urls import path
from .views import PrzedmiotApiView, TematApiView, PracaDomowaApiView

urlpatterns = [
    path("przedmioty/", PrzedmiotApiView.as_view(), name="przedmiot-list"),
    path("przedmioty/<int:pk>/", PrzedmiotApiView.as_view(), name="przedmiot-detail"),

    path("tematy/", TematApiView.as_view(), name="temat-list"),
    path("tematy/<int:pk>/", TematApiView.as_view(), name="temat-detail"),
    
    path("prace-domowe/", PracaDomowaApiView.as_view(), name="praca-list"),
    path("prace-domowe/<int:pk>/", PracaDomowaApiView.as_view(), name="praca-detail"),
]
