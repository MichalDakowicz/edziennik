from django.db import models
from django.contrib.auth.models import User

THEME_CHOICES = [
        ('light', 'Jasny'),
        ('dark', 'Ciemny'),
        ('system', 'Domyślny systemowy'),
    ]

# Minimal source constants used by Klasa.zrodlo field.
# Replace or extend these with real values from your project if available.
SOURCE_LOCAL = 'local'
SOURCE_EXTERNAL = 'external'
SOURCE_CHOICES = [
    (SOURCE_LOCAL, 'Local'),
    (SOURCE_EXTERNAL, 'External'),
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
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    theme_preference = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='system',
        help_text='Choose your preferred theme'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # TOTP (Google Authenticator) fields
    totp_secret = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text='Base32 secret used for TOTP with Google Authenticator'
    )
    totp_enabled = models.BooleanField(
        default=False,
        help_text='Whether TOTP 2FA is enabled for this user'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.get_theme_preference_display()}"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


    # Import audit module so its model classes are defined when Django loads app models.
    try:
        from . import audit  # noqa: F401
    except Exception:
        # If audit module fails to import, avoid breaking the models module import.
        pass


class Wiadomosc(models.Model):
    nadawca = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wyslane_wiadomosci')
    odbiorca = models.ForeignKey(User, on_delete=models.CASCADE, related_name='odebrane_wiadomosci')
    przeczytana = models.BooleanField(default=False)
    temat = models.CharField(max_length=255)
    tresc = models.TextField()
    data_wyslania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wiadomość od {self.nadawca.first_name} {self.nadawca.last_name} do {self.odbiorca.first_name} {self.odbiorca.last_name}"

    class Meta:
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"
        ordering = ['-data_wyslania']



class Klasa(models.Model):
    
    nazwa = models.CharField(max_length=10, null=True, blank=True)
    numer = models.IntegerField(null=True, blank=True)


    wychowawca = models.ForeignKey(Nauczyciel, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='prowadzone_klasy')
   

    objects = models.Manager()
    
    
    
    active = models.Manager()

    def __str__(self):
        
        if self.numer:
            return f"{self.numer} {self.nazwa}"
        return self.nazwa

   

    class Meta:
        verbose_name = "Klasa"
        verbose_name_plural = "Klasy"


class Adres(models.Model):
    ulica = models.CharField(max_length=200, blank=True, null=True)
    numer_domu = models.CharField(max_length=50, blank=True, null=True)
    numer_mieszkania = models.CharField(max_length=50, blank=True, null=True)
    miasto = models.CharField(max_length=100, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=20, blank=True, null=True)
    kraj = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        parts = [self.ulica or '', self.numer_domu or '', self.numer_mieszkania or '', self.miasto or '']
        return ', '.join([p for p in parts if p]) or 'Adres'