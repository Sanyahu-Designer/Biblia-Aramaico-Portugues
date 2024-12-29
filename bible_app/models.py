from django.db import models
from django.contrib.auth.models import User

__all__ = ['Book', 'Chapter', 'Verse', 'TraducaoEspecifica']

class Book(models.Model):
    name = models.CharField('Nome do Livro', max_length=100)
    order = models.IntegerField('Ordem', default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
    
    def __str__(self):
        return self.name

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    number = models.IntegerField('Número do Capítulo')
    
    class Meta:
        ordering = ['number']
        verbose_name = 'Capítulo'
        verbose_name_plural = 'Capítulos'
        unique_together = ['book', 'number']
    
    def __str__(self):
        return f"{self.book.name} - Capítulo {self.number}"

class Verse(models.Model):
    TRANSLATOR_CHOICES = [
        ('yosef_chaim', 'Yosef Chaim'),
        ('netzer_netzarim', 'Netzer Netzarim'),
    ]

    ARAMAIC_SOURCE_CHOICES = [
        ('curetonian', 'Antigos Evangelhos Curetonianos Siríacos'),
        ('sinaiticus', 'Palimpsesto Sinaítico Siríaco Antigo'),
        ('peshitta', 'Peshitta'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='verses')
    number = models.IntegerField('Número do Versículo')
    aramaic_text = models.TextField('Texto em Aramaico')
    portuguese_text = models.TextField('Texto em Português')
    translator_note = models.TextField('Nota do Tradutor', blank=True, null=True)
    translator = models.CharField('Tradutor', max_length=20, choices=TRANSLATOR_CHOICES)
    aramaic_source = models.CharField('Fonte do Texto Aramaico', max_length=20, choices=ARAMAIC_SOURCE_CHOICES)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        ordering = ['number']
        verbose_name = 'Versículo'
        verbose_name_plural = 'Versículos'
        unique_together = ['chapter', 'number']
    
    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.number}"