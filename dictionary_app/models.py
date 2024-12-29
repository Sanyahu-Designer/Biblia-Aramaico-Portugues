from django.db import models
from django.contrib.auth.models import User
from bible_app.models import Verse
from django.utils import timezone

class GrammaticalCategory(models.Model):
    name = models.CharField('Nome', max_length=100, unique=True)
    description = models.TextField('Descrição', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria Gramatical'
        verbose_name_plural = 'Categorias Gramaticais'
        ordering = ['name']

class AramaicWord(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('N', 'Neutro'),
    ]
    
    NUMBER_CHOICES = [
        ('S', 'Singular'),
        ('P', 'Plural'),
        ('D', 'Dual'),
    ]

    aramaic_word = models.CharField('Palavra em Aramaico', max_length=100)
    transliteration = models.CharField('Transliteração', max_length=100)
    portuguese_translation = models.CharField('Tradução em Português', max_length=200)
    root_word = models.CharField('Raiz da Palavra', max_length=100, blank=True, null=True)
    grammatical_category = models.ForeignKey(GrammaticalCategory, verbose_name='Categoria Gramatical', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField('Gênero', max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    number = models.CharField('Número', max_length=1, choices=NUMBER_CHOICES, blank=True, null=True)
    notes = models.TextField('Anotações', blank=True, null=True)
    created_at = models.DateTimeField('Data de Criação', default=timezone.now)
    updated_at = models.DateTimeField('Data de Atualização', auto_now=True)
    favorites = models.ManyToManyField(User, verbose_name='Favoritos', related_name='favorite_words', blank=True)

    def __str__(self):
        return f"{self.aramaic_word} ({self.transliteration})"

    class Meta:
        verbose_name = 'Palavra Aramaica'
        verbose_name_plural = 'Palavras Aramaicas'
        ordering = ['aramaic_word']

class WordOccurrence(models.Model):
    word = models.ForeignKey(AramaicWord, verbose_name='Palavra', on_delete=models.CASCADE, related_name='occurrences')
    verse = models.ForeignKey(Verse, verbose_name='Versículo', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)

    def __str__(self):
        return f"{self.word} em {self.verse.reference}"

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
        unique_together = ['word', 'verse']

class WordCrossReference(models.Model):
    word = models.ForeignKey(AramaicWord, verbose_name='Palavra', on_delete=models.CASCADE, related_name='cross_references')
    context = models.TextField('Contexto', null=True, blank=True)
    created_at = models.DateTimeField('Data de Criação', default=timezone.now)

    def __str__(self):
        return f"{self.word} - Contexto"

    class Meta:
        verbose_name = 'Referência Cruzada'
        verbose_name_plural = 'Referências Cruzadas'
        ordering = ['word']
