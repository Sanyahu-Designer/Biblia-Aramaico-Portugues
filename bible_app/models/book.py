"""Model for Bible books."""
from django.db import models

class Book(models.Model):
    name = models.CharField('Nome do Livro', max_length=100)
    order = models.IntegerField('Ordem', default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
    
    def __str__(self):
        return self.name