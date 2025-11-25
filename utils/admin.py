from django.contrib import admin
from .models import Przedmiot, Temat, PracaDomowa, DataSource


@admin.register(Przedmiot)
class PrzedmiotAdmin(admin.ModelAdmin):
	list_display = ("id", "nazwa", "nazwa_skrocona", "numer")


@admin.register(Temat)
class TematAdmin(admin.ModelAdmin):
	list_display = ("id", "tresc", "data", "przedmiot")


@admin.register(PracaDomowa)
class PracaDomowaAdmin(admin.ModelAdmin):
	list_display = ("id", "klasa", "przedmiot", "nauczyciel", "data_wystawienia")


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
	list_display = ("id", "active_source", "last_import_file", "last_imported_at")
