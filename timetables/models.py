from django.db import models

from users.models import Nauczyciel, Uczen

# Create your models here.
class PlanyZajec(models.Model):
    # klasa = models.ForeignKey(Klasa, on_delete=models.CASCADE, related_name='plany_zajec') # TODO: dodać klasę
    ObowiazujeOdDnia = models.DateField()
    wpisy = models.ManyToManyField('PlanWpis', related_name='plany_zajec', blank=True)
    class Meta:
        verbose_name_plural = "Plany Zajęć"

    def __str__(self):
        return f"Plan dla {self.klasa} od {self.ObowiazujeOdDnia}"
        
    

class GodzinyLekcyjne(models.Model):
    Numer = models.IntegerField()
    CzasOd = models.TimeField(max_length=45)
    CzasDo = models.TimeField(max_length=45)
    CzasTrwania = models.IntegerField() 

    class Meta:
        verbose_name_plural = "Godziny Lekcyjne"

    def __str__(self):
        return f"G.L. {self.Numer}: {self.CzasOd}-{self.CzasDo}"

class DniTygodnia(models.Model):
    Nazwa = models.CharField(max_length=45)
    Numer = models.IntegerField()

    class Meta:
        verbose_name_plural = "Dni Tygodnia"

    def __str__(self):
        return self.Nazwa


class Zajecia(models.Model):
    
    # przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE, related_name='zajecia_przedmiotu') # TODO: dodać przedmiot
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, related_name='zajecia_nauczyciela', null=True,blank=True,
    )

    class Meta:
        verbose_name_plural = "Zajęcia"

    def __str__(self):
        return f"{self.przedmiot} ({self.nauczyciel})"

class PlanWpis(models.Model):
    godzina_lekcyjna = models.ForeignKey(GodzinyLekcyjne, on_delete=models.CASCADE)
    dzien_tygodnia = models.ForeignKey(DniTygodnia, on_delete=models.CASCADE)
    zajecia = models.ForeignKey(Zajecia, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name_plural = "Wpisy do Planu"

    def __str__(self):
        
        return f"Wpis {self.pk}"
    


class Wydarzenie(models.Model):
    tytul = models.CharField(max_length=200)
    opis = models.TextField()
    data = models.DateTimeField()
    
    #klasa = models.ForeignKey('Klasa', on_delete=models.CASCADE, related_name='wydarzenia', null=True, blank=True)
    #przedmiot = models.ForeignKey('Przedmiot', on_delete=models.CASCADE, related_name='wydarzenia', null=True, blank=True)
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.CASCADE, related_name='wydarzenia', null=True, blank=True)

    
    objects = models.Manager()
    active = models.Manager()

    def __str__(self):
        return f"Wydarzenie: {self.tytul} - {self.data.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"
        ordering = ['-data']


