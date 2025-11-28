from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
	User,
	Uczen,
	Nauczyciel,
	Rodzic,
	UserProfile,
	Wiadomosc,
	Klasa,
	Adres,
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "user_id")



@admin.register(Uczen)
class UczenAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "telefon", "data_urodzenia")


@admin.register(Nauczyciel)
class NauczycielAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "telefon")


@admin.register(Rodzic)
class RodzicAdmin(admin.ModelAdmin):
	list_display = ("id", "user",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "theme_preference", "created_at")


@admin.register(Wiadomosc)
class WiadomoscAdmin(admin.ModelAdmin):
	list_display = ("id", "nadawca", "odbiorca", "przeczytana", "data_wyslania")


@admin.register(Klasa)
class KlasaAdmin(admin.ModelAdmin):
	list_display = ("id", "nazwa", "numer", "wychowawca")


@admin.register(Adres)
class AdresAdmin(admin.ModelAdmin):
	list_display = ("id", "ulica", "miasto", "kod_pocztowy")
