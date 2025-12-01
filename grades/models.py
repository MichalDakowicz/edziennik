from django.db import models

from users.models import Nauczyciel, Uczen

from utils.models import Przedmiot

# Create your models here.


class ActiveSourceManager(models.Manager):
    pass
class Ocena(models.Model):
    wartosc = models.DecimalField(max_digits=3, decimal_places=2)
    waga = models.PositiveSmallIntegerField(default=1)
    
    opis = models.CharField(max_length=200, blank=True, null=True)
    data_wystawienia = models.DateTimeField(auto_now_add=True)
    
    czy_punkty=models.BooleanField(default=False)
    czy_opisowa=models.BooleanField(default=False)
    czy_do_sredniej=models.BooleanField(default=True)
    
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='oceny')
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.CASCADE, related_name='wystawione_oceny')
    
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE, related_name='oceny')
    
    def __str__(self):
        return f"{self.wartosc} - {self.uczen} ({self.przedmiot})"

    class Meta:
        verbose_name = "Ocena"
        verbose_name_plural = "Oceny"
        ordering = ['-data_wystawienia']
        
        
class OcenaOkresowa(models.Model):
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='oceny_okresowe')
    
    wartosc = models.DecimalField(max_digits=3, decimal_places=2)

    okres = models.IntegerField()  # 1 dla pierwszego okresu, 2 dla drugiego, itp.
    # Make przedmiot nullable to avoid requiring a one-off default when applying migrations
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE, related_name='oceny_okresowe', null=True, blank=True)

    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Ocena okresowa"
        verbose_name_plural = "Oceny okresowe"

    def __str__(self):
        # guard against deployments where the model on disk/db may not have
        # the `przedmiot` attribute (older migrations or differing code); use
        # getattr to avoid AttributeError in admin/list views.
        przedmiot = getattr(self, 'przedmiot', None)
        przedmiot_str = str(przedmiot) if przedmiot else "-"
        return f"{self.uczen} - {przedmiot_str}: {self.wartosc} ({self.okres})"
    
        
class OcenaKoncowa(models.Model):
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='oceny_koncowe')
    
    wartosc = models.DecimalField(max_digits=3, decimal_places=2) 
    
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE, related_name='oceny_koncowe')
    
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Ocena końcowa"
        verbose_name_plural = "Oceny końcowe"

    def __str__(self):
        return f"{self.uczen} - ({self.przedmiot}): {self.wartosc}"

class ZachowaniePunkty(models.Model):
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE, related_name='punkty_zachowania')
    punkty = models.IntegerField()
    opis = models.TextField(blank=True, null=True)
    data_wpisu = models.DateTimeField(auto_now_add=True)
    nauczyciel_wpisujacy = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, null=True,
                                             related_name='wpisane_punkty_zachowania')
   

    objects = models.Manager()
    
    active = ActiveSourceManager()

    def __str__(self):
        znak = "+" if self.punkty > 0 else ""
        return f"{self.uczen} - {znak}{self.punkty} pkt ({self.data_wpisu.strftime('%Y-%m-%d')})"

    class Meta:
        verbose_name = "Punkt z zachowania"
        verbose_name_plural = "Punkty z zachowania"
        ordering = ['-data_wpisu']

