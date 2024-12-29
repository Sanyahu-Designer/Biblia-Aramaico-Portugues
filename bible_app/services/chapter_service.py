"""Service for handling Chapter-related operations."""
from django.db.models import QuerySet
from ..models import Chapter, Book

class ChapterService:
    @staticmethod
    def get_chapters_by_book(book_id: int) -> list:
        """Get all chapters for a specific book.
        
        Args:
            book_id (int): ID of the book
            
        Returns:
            list: List of chapters with their IDs and numbers
        """
        chapters = Chapter.objects.filter(book_id=book_id).order_by('number')
        return [{'id': chapter.id, 'number': chapter.number} for chapter in chapters]
    
    @staticmethod
    def get_chapter_by_id(chapter_id: int) -> Chapter:
        """Get a specific chapter by ID."""
        return Chapter.objects.get(id=chapter_id)
    
    @staticmethod
    def create_chapter(book: Book, number: int) -> Chapter:
        """Create a new chapter for a book."""
        return Chapter.objects.create(book=book, number=number)
    
    @staticmethod
    def get_next_chapter_number(book_id: int) -> int:
        """Get the next available chapter number for a book."""
        last_chapter = Chapter.objects.filter(book_id=book_id).order_by('-number').first()
        return (last_chapter.number + 1) if last_chapter else 1