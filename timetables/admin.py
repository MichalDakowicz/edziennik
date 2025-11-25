from django.contrib import admin
from .models import (
	PlanyZajec,
	GodzinyLekcyjne,
	DniTygodnia,
	Zajecia,
	PlanWpis,
	Wydarzenie,
)


@admin.register(PlanyZajec)
class PlanyZajecAdmin(admin.ModelAdmin):
	list_display = ("id", "ObowiazujeOdDnia")


@admin.register(GodzinyLekcyjne)
class GodzinyLekcyjneAdmin(admin.ModelAdmin):
	list_display = ("id", "Numer", "CzasOd", "CzasDo")


@admin.register(DniTygodnia)
class DniTygodniaAdmin(admin.ModelAdmin):
	list_display = ("id", "Nazwa", "Numer")


@admin.register(Zajecia)
class ZajeciaAdmin(admin.ModelAdmin):
	list_display = ("id", "nauczyciel")


@admin.register(PlanWpis)
class PlanWpisAdmin(admin.ModelAdmin):
	list_display = ("id", "godzina_lekcyjna", "dzien_tygodnia", "zajecia")


@admin.register(Wydarzenie)
class WydarzenieAdmin(admin.ModelAdmin):
	list_display = ("id", "tytul", "nauczyciel", "data")
