"""User preferences model."""
from django.db import models
from django.contrib.auth.models import User

class UserPreference(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    font_size = models.IntegerField(default=16)
    show_transliteration = models.BooleanField(default=True)
    show_pronunciation = models.BooleanField(default=True)
    show_word_analysis = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Preferência do Usuário'
        verbose_name_plural = 'Preferências dos Usuários'

    def __str__(self):
        return f'Preferências de {self.user.username}'