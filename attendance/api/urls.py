from django.urls import path
from .views import StatusApiView, FrekwencjaApiView

urlpatterns = [
	path("statusy/", StatusApiView.as_view(), name="status-list"),
	path("statusy/<int:pk>/", StatusApiView.as_view(), name="status-detail"),

	path("frekwencja/", FrekwencjaApiView.as_view(), name="frekwencja-list"),
	path("frekwencja/<int:pk>/", FrekwencjaApiView.as_view(), name="frekwencja-detail"),
]
