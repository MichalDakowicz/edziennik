from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ocena
from .forms import OcenaForm
from users.models import Nauczyciel


class AddGradeView(LoginRequiredMixin, View):
    """View for adding a new grade."""

    template_name = "grades/add_grade.html"
    login_url = "/admin/login/"

    def get(self, request):
        form = OcenaForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # Try to get the teacher associated with the current user
        nauczyciel = None
        try:
            nauczyciel = Nauczyciel.objects.get(user=request.user)
        except Nauczyciel.DoesNotExist:
            pass

        form = OcenaForm(request.POST, nauczyciel=nauczyciel)

        if form.is_valid():
            ocena = form.save()
            messages.success(
                request,
                f"Ocena {ocena.wartosc} dla ucznia {ocena.uczen} została dodana pomyślnie!",
            )
            return redirect("grades:grade_list")

        return render(request, self.template_name, {"form": form})


class GradeListView(LoginRequiredMixin, View):
    """View for displaying the list of grades."""

    template_name = "grades/grade_list.html"
    login_url = "/admin/login/"

    def get(self, request):
        oceny = Ocena.objects.select_related(
            "uczen",
            "uczen__user",
            "uczen__klasa",
            "przedmiot",
            "nauczyciel",
            "nauczyciel__user",
        ).order_by("-data_wystawienia")[
            :50
        ]  # Limit to last 50 grades

        return render(request, self.template_name, {"oceny": oceny})


# Function-based views alternative (simpler approach)
def add_grade_view(request):
    """Function-based view for adding a new grade."""
    if request.method == "POST":
        nauczyciel = None
        try:
            nauczyciel = Nauczyciel.objects.get(user=request.user)
        except (Nauczyciel.DoesNotExist, AttributeError):
            pass

        form = OcenaForm(request.POST, nauczyciel=nauczyciel)

        if form.is_valid():
            ocena = form.save()
            messages.success(
                request,
                f"Ocena {ocena.wartosc} dla ucznia {ocena.uczen} została dodana pomyślnie!",
            )
            return redirect("grades:grade_list")
    else:
        form = OcenaForm()

    return render(request, "grades/add_grade.html", {"form": form})


def grade_list_view(request):
    """Function-based view for displaying the list of grades."""
    oceny = Ocena.objects.select_related(
        "uczen",
        "uczen__user",
        "uczen__klasa",
        "przedmiot",
        "nauczyciel",
        "nauczyciel__user",
    ).order_by("-data_wystawienia")[:50]

    return render(request, "grades/grade_list.html", {"oceny": oceny})
