"""Model for Bible chapters."""
from django.db import models

class Chapter(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='chapters')
    number = models.IntegerField('Número do Capítulo')
    
    class Meta:
        ordering = ['number']
        verbose_name = 'Capítulo'
        verbose_name_plural = 'Capítulos'
        unique_together = ['book', 'number']
    
    def __str__(self):
        return f"{self.book.name} - Capítulo {self.number}"
        
    def debug_verses(self):
        """Debug method to check verses."""
        verses = self.verses.all()
        print(f"DEBUG - Chapter {self.number} verses:")
        print(f"  - Total verses: {verses.count()}")
        for verse in verses[:3]:  # Show first 3 verses
            print(f"  - Verse {verse.number}:")
            print(f"    * ID: {verse.id}")
            print(f"    * Aramaic: {verse.aramaic_text[:50] if verse.aramaic_text else 'None'}")
            print(f"    * Portuguese: {verse.portuguese_text[:50] if verse.portuguese_text else 'None'}")
        return verses