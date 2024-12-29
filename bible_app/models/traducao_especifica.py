"""Model for specific word translations."""
from django.db import models

class TraducaoEspecifica(models.Model):
    termo_original = models.CharField('Termo Original', max_length=100, unique=True)
    traducao = models.CharField('Tradução', max_length=100)
    notas = models.TextField('Notas', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Tradução Específica'
        verbose_name_plural = 'Traduções Específicas'
        ordering = ['termo_original']

    def __str__(self):
        return f"{self.termo_original} → {self.traducao}"