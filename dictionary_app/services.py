from django.db.models import Count
from bible_app.models import Verse
from .models import WordOccurrence
import re

class WordOccurrenceService:
    @staticmethod
    def detect_word_occurrences(word):
        """
        Detecta ocorrências de uma palavra em versículos usando o mesmo sistema do tooltip.
        
        Args:
            word (str): A palavra em aramaico para procurar
            
        Returns:
            dict: Um dicionário contendo o total de ocorrências e uma lista de ocorrências
        """
        # Primeiro faz uma busca inicial para reduzir o conjunto de versículos
        verses = Verse.objects.filter(aramaic_text__icontains=word).select_related('chapter', 'chapter__book')
        
        # Prepara a resposta
        occurrences = []
        
        # Regex para encontrar a palavra com ou sem pontuação
        # Inclui caracteres de pontuação aramaica e hebraica
        pattern = re.compile(rf'\b{re.escape(word)}[\u0591-\u05C7\u0700-\u074F]*\b')
        
        for verse in verses:
            # Procura todas as ocorrências da palavra no versículo
            matches = pattern.finditer(verse.aramaic_text)
            
            for match in matches:
                # Obtém o contexto (texto antes e depois da palavra)
                start = max(0, match.start() - 50)
                end = min(len(verse.aramaic_text), match.end() + 50)
                context = verse.aramaic_text[start:end]
                
                occurrences.append({
                    'book': verse.chapter.book.name,
                    'chapter': verse.chapter.number,
                    'verse': verse.number,
                    'reference': f"{verse.chapter.book.name} {verse.chapter.number}:{verse.number}",
                    'text': context,
                    'word_position': (match.start() - start, match.end() - start)
                })
        
        return {
            'total': len(occurrences),
            'occurrences': occurrences
        }

    @staticmethod
    def get_word_statistics(word_id):
        """
        Obtém estatísticas de ocorrências de uma palavra.
        
        Args:
            word_id (int): ID da palavra
            
        Returns:
            dict: Um dicionário com estatísticas da palavra
        """
        occurrences = WordOccurrence.objects.filter(word_id=word_id).select_related(
            'verse', 'verse__chapter', 'verse__chapter__book'
        )
        
        # Lista de versículos
        verses = []
        book_stats = {}
        
        for occ in occurrences:
            book_name = occ.verse.chapter.book.name
            book_stats[book_name] = book_stats.get(book_name, 0) + 1
            
            verses.append({
                'reference': f"{book_name} {occ.verse.chapter.number}:{occ.verse.number}",
                'text': occ.verse.aramaic_text
            })
        
        return {
            'total': occurrences.count(),
            'by_book': [
                {'book': book, 'count': count}
                for book, count in sorted(book_stats.items(), key=lambda x: (-x[1], x[0]))
            ],
            'verses': verses
        }
