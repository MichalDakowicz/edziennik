from rest_framework import routers
from users.api.urls import router as users_router
from grades.api.urls import router as grades_router
from timetables.api.urls import router as timetables_router
from attendance.api.urls import router as attendance_router
from utils.api.urls import router as utils_router
from django.urls import path, include

router = routers.DefaultRouter()
router.registry.extend(users_router.registry)
router.registry.extend(grades_router.registry)
router.registry.extend(timetables_router.registry)
router.registry.extend(attendance_router.registry)
router.registry.extend(utils_router.registry)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("authentication.api.urls")),
]
