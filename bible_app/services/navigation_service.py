"""Service for handling Bible navigation logic."""
from django.db.models import QuerySet
from ..models import Book, Chapter
from ..utils.cache_utils import cache_navigation
from .book_navigation import BookNavigationService
from .chapter_navigation import ChapterNavigationService

class NavigationService:
    def __init__(self):
        self.book_navigation = BookNavigationService()
        self.chapter_navigation = ChapterNavigationService()

    @cache_navigation()
    def get_adjacent_chapters(self, chapter_id: int) -> dict:
        """Get previous and next chapters for navigation.
            
        Args:
            chapter_id (int): Current chapter ID
                
        Returns:
            dict: Dictionary containing previous and next chapters
        """
        try:
            current_chapter = Chapter.objects.select_related('book').get(id=chapter_id)
        except Chapter.DoesNotExist:
            return {
                'previous_chapter': None,
                'next_chapter': None
            }
            
        previous_chapter = self.chapter_navigation.get_previous_chapter(current_chapter)
        if not previous_chapter:
            previous_book = self.book_navigation.get_previous_book(current_chapter.book)
            if previous_book:
                previous_chapter = self.chapter_navigation.get_last_chapter(previous_book)
            
        next_chapter = self.chapter_navigation.get_next_chapter(current_chapter)
        if not next_chapter:
            next_book = self.book_navigation.get_next_book(current_chapter.book)
            if next_book:
                next_chapter = self.chapter_navigation.get_first_chapter(next_book)
            
        return {
            'previous_chapter': previous_chapter,
            'next_chapter': next_chapter
        }