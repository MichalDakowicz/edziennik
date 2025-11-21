from django.urls import path
from .views import UczenApiView

urlpatterns = [
    path("uczniowie/", UczenApiView.as_view(), name="uczen-list"),
    path("uczniowie/<int:pk>/", UczenApiView.as_view(), name="uczen-detail"),
]
