from django.db import models

from users.models import Klasa, Nauczyciel
from django.utils import timezone

# Create your models here.
 
# Minimal source choices used by DataSource. The project previously referenced
# these constants; define safe defaults so imports and system checks succeed.
SOURCE_LOCAL = 'local'
SOURCE_EXTERNAL = 'external'
SOURCE_CHOICES = [
    (SOURCE_LOCAL, 'Local'),
    (SOURCE_EXTERNAL, 'External'),
]


class Przedmiot(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    nazwa_skrocona = models.CharField(max_length=50, blank=True, null=True) 
    numer=models.IntegerField(null=True, blank=True)
    czy_dodatkowy = models.BooleanField(default=False)
    nauczyciele = models.ManyToManyField(Nauczyciel, related_name='przedmioty', blank=True)
    

    objects = models.Manager()
    active = models.Manager()

    def __str__(self):
        return f"{self.nazwa}"

    class Meta:
        verbose_name = "Przedmiot"
        verbose_name_plural = "Przedmioty"

class Temat(models.Model):
    tresc = models.CharField(max_length=200, blank=True, null=True)
    data = models.DateField(null=True, blank=True)
    numer_lekcji = models.IntegerField(null=True, blank=True)
    czas_realizacji = models.IntegerField(null=True, blank=True, help_text='Czas realizacji w minutach')
    czas_od = models.TimeField(null=True, blank=True)
    czas_do = models.TimeField(null=True, blank=True)
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.SET_NULL, null=True, blank=True)
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        
        return (self.tresc or '')[:50] or 'Temat'
    

class PracaDomowa(models.Model):
    klasa = models.ForeignKey(Klasa, on_delete=models.CASCADE, related_name='prace_domowe')
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE, related_name='prace_domowe')
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.CASCADE, related_name='prace_domowe')
    opis = models.TextField()
    data_wystawienia = models.DateTimeField(auto_now_add=True)
    termin = models.DateField()
    
    objects = models.Manager()
    # fallback to default manager if custom ActiveSourceManager isn't available here
    active = models.Manager()

    def __str__(self):
        return f"Praca domowa z {self.przedmiot} dla klasy {self.klasa} - {self.data_wystawienia.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Praca domowa"
        verbose_name_plural = "Prace domowe"
        ordering = ['-data_wystawienia']

    
class DataSource(models.Model):
    active_source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_LOCAL)
    last_import_file = models.CharField(max_length=255, blank=True, null=True)
    last_imported_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Active: {self.active_source}"

    @classmethod
    def get_active(cls):
        # use module-level constant SOURCE_LOCAL instead of cls.SOURCE_LOCAL
        obj, _ = cls.objects.get_or_create(pk=1, defaults={'active_source': SOURCE_LOCAL})
        return obj.active_source

    @classmethod
    def set_active(cls, source, filename=None):
        obj, _ = cls.objects.get_or_create(pk=1)
        obj.active_source = source
        if filename:
            obj.last_import_file = filename
            obj.last_imported_at = timezone.now()
        obj.save()
        return obj
