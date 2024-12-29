"""Service for handling Book-related operations."""
from django.db.models import QuerySet
from ..models import Book
from ..utils.cache_utils import cache_static_data

class BookService:
    @staticmethod
    @cache_static_data()
    def get_all_books() -> QuerySet:
        """Get all books ordered by their order field."""
        return Book.objects.all().order_by('order')
    
    @staticmethod
    def get_book_by_id(book_id: int) -> Book:
        """Get a specific book by ID."""
        return Book.objects.get(id=book_id)
    
    @staticmethod
    def create_book(name: str, order: int) -> Book:
        """Create a new book."""
        return Book.objects.create(name=name, order=order)