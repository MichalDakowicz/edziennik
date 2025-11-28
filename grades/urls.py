from django.urls import path
from . import views

app_name = "grades"

urlpatterns = [
    path("add/", views.AddGradeView.as_view(), name="add_grade"),
    path("", views.GradeListView.as_view(), name="grade_list"),
    # Alternative function-based views (uncomment to use instead)
    # path('add/', views.add_grade_view, name='add_grade'),
    # path('', views.grade_list_view, name='grade_list'),
]
