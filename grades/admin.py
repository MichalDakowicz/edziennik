from django.contrib import admin
from .models import (
	Ocena,
	OcenaOkresowa,
	OcenaKoncowa,
	ZachowaniePunkty,
)


@admin.register(Ocena)
class OcenaAdmin(admin.ModelAdmin):
	list_display = ("id", "wartosc", "uczen", "nauczyciel", "data_wystawienia")


@admin.register(OcenaOkresowa)
class OcenaOkresowaAdmin(admin.ModelAdmin):
	list_display = ("id", "uczen", "wartosc", "okres")


@admin.register(OcenaKoncowa)
class OcenaKoncowaAdmin(admin.ModelAdmin):
	list_display = ("id", "uczen", "wartosc")


@admin.register(ZachowaniePunkty)
class ZachowaniePunktyAdmin(admin.ModelAdmin):
	list_display = ("id", "uczen", "punkty", "nauczyciel_wpisujacy", "data_wpisu")
