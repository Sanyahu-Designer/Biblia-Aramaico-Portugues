"""Service for handling book navigation."""
from django.db.models import QuerySet
from ..models import Book

class BookNavigationService:
    def get_previous_book(self, current_book: Book) -> Book:
        """Get the previous book based on order.
        
        Args:
            current_book (Book): Current book
            
        Returns:
            Book: Previous book or None if not found
        """
        return Book.objects.filter(
            order__lt=current_book.order
        ).order_by('-order').first()
    
    def get_next_book(self, current_book: Book) -> Book:
        """Get the next book based on order.
        
        Args:
            current_book (Book): Current book
            
        Returns:
            Book: Next book or None if not found
        """
        return Book.objects.filter(
            order__gt=current_book.order
        ).order_by('order').first()