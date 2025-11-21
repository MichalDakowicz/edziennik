from django.urls import path
from .views import UczenApiView, NauczycielApiView, RodzicApiView, UserProfileApiView

urlpatterns = [
    path("uczniowie/", UczenApiView.as_view(), name="uczen-list"),
    path("uczniowie/<int:pk>/", UczenApiView.as_view(), name="uczen-detail"),
    
    path("nauczyciele/", NauczycielApiView.as_view(), name="nauczyciel-list"),
    path("nauczyciele/<int:pk>/", NauczycielApiView.as_view(), name="nauczyciel-detail"),
    
    path("rodzice/", RodzicApiView.as_view(), name="rodzic-list"),
    path("rodzice/<int:pk>/", RodzicApiView.as_view(), name="rodzic-detail"),
    
    path("userprofiles/", UserProfileApiView.as_view(), name="userprofile-list"),
    path("userprofiles/<int:pk>/", UserProfileApiView.as_view(), name="userprofile-detail"),
]
