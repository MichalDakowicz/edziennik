from django import forms
from .models import Ocena
from users.models import Uczen, Nauczyciel
from utils.models import Przedmiot


class OcenaForm(forms.ModelForm):
    """Form for adding a new grade (Ocena) to a student."""

    class Meta:
        model = Ocena
        fields = [
            "uczen",
            "przedmiot",
            "wartosc",
            "waga",
            "opis",
            "czy_punkty",
            "czy_opisowa",
            "czy_do_sredniej",
        ]
        widgets = {
            "uczen": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_uczen",
                }
            ),
            "przedmiot": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_przedmiot",
                }
            ),
            "wartosc": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "1",
                    "max": "6",
                    "placeholder": "np. 4.50",
                }
            ),
            "waga": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "max": "10",
                    "placeholder": "Waga oceny (1-10)",
                }
            ),
            "opis": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Opis oceny (np. sprawdzian, kartkówka...)",
                }
            ),
            "czy_punkty": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "czy_opisowa": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "czy_do_sredniej": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }
        labels = {
            "uczen": "Uczeń",
            "przedmiot": "Przedmiot",
            "wartosc": "Wartość oceny",
            "waga": "Waga",
            "opis": "Opis",
            "czy_punkty": "Czy punktowa",
            "czy_opisowa": "Czy opisowa",
            "czy_do_sredniej": "Czy liczy się do średniej",
        }

    def __init__(self, *args, **kwargs):
        self.nauczyciel = kwargs.pop("nauczyciel", None)
        super().__init__(*args, **kwargs)

        # Order students by class and name
        self.fields["uczen"].queryset = Uczen.objects.select_related(
            "user", "klasa"
        ).order_by(
            "klasa__numer", "klasa__nazwa", "user__last_name", "user__first_name"
        )

        # Order subjects alphabetically
        self.fields["przedmiot"].queryset = Przedmiot.objects.all().order_by("nazwa")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.nauczyciel:
            instance.nauczyciel = self.nauczyciel
        if commit:
            instance.save()
        return instance
