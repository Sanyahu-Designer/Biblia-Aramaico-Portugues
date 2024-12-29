"""Service for handling verse-related operations."""
from django.db.models import QuerySet
from ..models import Verse
from ..utils.query_utils import filter_by_text, paginate_queryset

class VerseService:
    @staticmethod
    def get_verses_by_chapter(chapter_id: int) -> QuerySet:
        """Retrieve verses for a specific chapter with related data.
        
        Args:
            chapter_id (int): ID of the chapter
            
        Returns:
            QuerySet: Queryset of verses with related book and chapter data
        """
        return Verse.objects.filter(
            chapter_id=chapter_id
        ).select_related('chapter', 'chapter__book')
    
    @staticmethod
    def search_verses(search_text: str, page: int = 1) -> QuerySet:
        """Search verses by text in both Aramaic and Portuguese.
        
        Args:
            search_text (str): Text to search for
            page (int): Page number for pagination
            
        Returns:
            QuerySet: Filtered and paginated queryset of verses
        """
        verses = Verse.objects.select_related('chapter', 'chapter__book')
        verses = filter_by_text(
            verses, 
            search_text, 
            ['aramaic_text', 'portuguese_text', 'translator_note']
        )
        return paginate_queryset(verses, page)

    @staticmethod
    def create_verse(chapter, number: int, aramaic_text: str, portuguese_text: str, 
                    translator: str, translator_note: str = None) -> Verse:
        """Create a new verse.
        
        Args:
            chapter: Chapter instance
            number (int): Verse number
            aramaic_text (str): Aramaic text
            portuguese_text (str): Portuguese text
            translator (str): Translator identifier
            translator_note (str, optional): Translator's note
            
        Returns:
            Verse: Created verse instance
        """
        return Verse.objects.create(
            chapter=chapter,
            number=number,
            aramaic_text=aramaic_text,
            portuguese_text=portuguese_text,
            translator=translator,
            translator_note=translator_note
        )

    @staticmethod
    def get_next_verse_number(chapter_id: int) -> int:
        """Get the next available verse number for a chapter."""
        last_verse = Verse.objects.filter(chapter_id=chapter_id).order_by('-number').first()
        return (last_verse.number + 1) if last_verse else 1