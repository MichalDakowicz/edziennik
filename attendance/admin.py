from django.contrib import admin
from .models import (
	StatusyObecnosci,
	Frekwencja,
)


@admin.register(StatusyObecnosci)
class StatusyObecnosciAdmin(admin.ModelAdmin):
	list_display = ("id", "Wartosc")


@admin.register(Frekwencja)
class FrekwencjaAdmin(admin.ModelAdmin):
	list_display = ("id", "Data", "uczen", "godzina_lekcyjna", "status")
