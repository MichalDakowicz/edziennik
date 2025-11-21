from django.urls import path
from .views import OcenaApiView, OcenaOkresowaApiView, OcenaKoncowaApiView

urlpatterns = [
    path("oceny/", OcenaApiView.as_view(), name="ocena-list"),
    path("oceny/<int:pk>/", OcenaApiView.as_view(), name="ocena-detail"),

    path("oceny-okresowe/", OcenaOkresowaApiView.as_view(), name="ocena-okresowa-list"),
    path("oceny-okresowe/<int:pk>/", OcenaOkresowaApiView.as_view(), name="ocena-okresowa-detail"),
    
    path("oceny-koncowe/", OcenaKoncowaApiView.as_view(), name="ocena-koncowa-list"),
    path("oceny-koncowe/<int:pk>/", OcenaKoncowaApiView.as_view(), name="ocena-koncowa-detail"),
]