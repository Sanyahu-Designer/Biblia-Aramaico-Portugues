"""Service for handling Aramaic word analysis."""
from django.db.models import QuerySet
from ..models import AramaicWord

class AramaicWordService:
    @staticmethod
    def get_word_details(word: str) -> AramaicWord:
        """Get details for an Aramaic word."""
        return AramaicWord.objects.get(word=word)
    
    @staticmethod
    def search_words(query: str) -> QuerySet:
        """Search Aramaic words."""
        return AramaicWord.objects.filter(
            word__icontains=query
        ) | AramaicWord.objects.filter(
            transliteration__icontains=query
        )
    
    @staticmethod
    def create_word(word: str, transliteration: str, definition: str, 
                   pronunciation_url: str = None) -> AramaicWord:
        """Create a new Aramaic word entry."""
        return AramaicWord.objects.create(
            word=word,
            transliteration=transliteration,
            definition=definition,
            pronunciation_url=pronunciation_url
        )