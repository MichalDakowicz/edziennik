from django.db import models

from timetables.models import GodzinyLekcyjne
from users.models import Uczen



class StatusyObecnosci(models.Model):
    Wartosc = models.CharField(max_length=45)
    class Meta:
        verbose_name_plural = "Statusy Obecności"

    def __str__(self):
        return self.Wartosc


class Frekwencja(models.Model):
    Data = models.DateField() 
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='frekwencja')
    godzina_lekcyjna = models.ForeignKey(GodzinyLekcyjne, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(StatusyObecnosci, on_delete=models.SET_NULL, null=True, blank=True, related_name='frekwencja')

    class Meta:
        verbose_name_plural = "Frekwencja"

    def __str__(self):
        status_info = str(self.status) if self.status else '?'
        return f"Frekwencja {self.uczen} - {self.Data} ({status_info})"



# Create your models here.
