from django.db import models

from users.models import Nauczyciel, Uczen

# Create your models here.
class Ocena(models.Model):
    wartosc = models.DecimalField(max_digits=3, decimal_places=2)
    waga = models.PositiveSmallIntegerField(default=1)
    
    opis = models.CharField(max_length=200, blank=True, null=True)
    data_wystawienia = models.DateTimeField(auto_now_add=True)
    
    czy_punkty=models.BooleanField(default=False)
    czy_opisowa=models.BooleanField(default=False)
    czy_do_sredniej=models.BooleanField(default=True)
    
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='oceny')
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, null=True, related_name='wystawione_oceny')
    
    # przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE, related_name='oceny')
    
    def __str__(self):
        return f"{self.wartosc} - {self.uczen} ({self.przedmiot})"

    class Meta:
        verbose_name = "Ocena"
        verbose_name_plural = "Oceny"
        ordering = ['-data_wystawienia']
        
        
class OcenaKoncowa(models.Model):
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='oceny_koncowe')
    
    wartosc = models.DecimalField(max_digits=3, decimal_places=2) 
    
    # przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE, related_name='oceny_koncowe')
    
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Ocena końcowa"
        verbose_name_plural = "Oceny końcowe"

    def __str__(self):
        return f"{self.uczen} - (przedmiot): {self.wartosc}" # TODO: dodać przedmiot


class OcenaOkresowa(models.Model):
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='oceny_okresowe')
    
    wartosc = models.DecimalField(max_digits=3, decimal_places=2)

    okres = models.IntegerField()  # 1 dla pierwszego okresu, 2 dla drugiego, itp.
    # przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE, related_name='oceny_okresowe')

    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Ocena okresowa"
        verbose_name_plural = "Oceny okresowe"

    def __str__(self):
        return f"{self.uczen} - {self.przedmiot}: {self.wartosc} ({self.okres})"