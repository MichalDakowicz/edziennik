from django.db import models
from django.contrib.auth.models import User

THEME_CHOICES = [
        ('light', 'Jasny'),
        ('dark', 'Ciemny'),
        ('system', 'Domyślny systemowy'),
    ]

# Create your models here.
class Uczen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # klasa = models.ForeignKey(Klasa, on_delete=models.SET_NULL, null=True, blank=True, related_name='uczniowie')

    telefon = models.CharField(max_length=20, null=True, blank=True)
    data_urodzenia = models.DateField()
    # adres = models.ForeignKey(Adres, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"  # TODO: dodać klasę

    class Meta:
        verbose_name = "Uczeń"
        verbose_name_plural = "Uczniowie"


class Nauczyciel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    telefon = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Nauczyciel"
        verbose_name_plural = "Nauczyciele"


class Rodzic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    telefon = models.CharField(max_length=20)
    
    dzieci = models.ManyToManyField(Uczen, related_name="rodzice")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    theme_preference = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='system',
    )
    
    def __str__(self):
        return f"Profil użytkownika: {self.user.username}"
    
    class Meta:
        verbose_name = "Profil Użytkownika"
        verbose_name_plural = "Profile Użytkowników"