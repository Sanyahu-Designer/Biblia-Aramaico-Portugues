"""Service for handling chapter navigation."""
from django.db.models import QuerySet
from ..models import Book, Chapter

class ChapterNavigationService:
    def get_previous_chapter(self, current_chapter: Chapter) -> Chapter:
        """Get the previous chapter in the same book.
        
        Args:
            current_chapter (Chapter): Current chapter
            
        Returns:
            Chapter: Previous chapter or None if not found
        """
        return Chapter.objects.filter(
            book=current_chapter.book,
            number__lt=current_chapter.number
        ).order_by('-number').first()
    
    def get_next_chapter(self, current_chapter: Chapter) -> Chapter:
        """Get the next chapter in the same book.
        
        Args:
            current_chapter (Chapter): Current chapter
            
        Returns:
            Chapter: Next chapter or None if not found
        """
        return Chapter.objects.filter(
            book=current_chapter.book,
            number__gt=current_chapter.number
        ).order_by('number').first()
    
    def get_first_chapter(self, book: Book) -> Chapter:
        """Get the first chapter of a book.
        
        Args:
            book (Book): Book instance
            
        Returns:
            Chapter: First chapter or None if not found
        """
        return Chapter.objects.filter(book=book).order_by('number').first()
    
    def get_last_chapter(self, book: Book) -> Chapter:
        """Get the last chapter of a book.
        
        Args:
            book (Book): Book instance
            
        Returns:
            Chapter: Last chapter or None if not found
        """
        return Chapter.objects.filter(book=book).order_by('-number').first()