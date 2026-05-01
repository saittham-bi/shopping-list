from django.db import models
from django.contrib.auth.models import User


class Laden(models.Model):
    name = models.CharField(max_length=100, unique=True)
    reihenfolge = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Laden'
        verbose_name_plural = 'Läden'
        ordering = ['reihenfolge', 'name']

    def __str__(self):
        return self.name


class Einkauf(models.Model):
    artikel = models.CharField(max_length=200, verbose_name='Artikel')
    gekauft = models.BooleanField(default=False, verbose_name='Gekauft')
    laden = models.ForeignKey(
        Laden,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Laden',
        related_name='einkäufe'
    )
    geaendert = models.DateTimeField(auto_now=True, verbose_name='Geändert')
    erstellt = models.DateTimeField(auto_now_add=True, verbose_name='Erstellt')
    erstellt_von = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='einkäufe',
        verbose_name='Erstellt von'
    )

    class Meta:
        verbose_name = 'Einkauf'
        verbose_name_plural = 'Einkäufe'
        ordering = ['laden__reihenfolge', 'laden__name', 'artikel']

    def __str__(self):
        return self.artikel
