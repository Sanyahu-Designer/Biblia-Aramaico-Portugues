"""Service for handling bookmarks."""
from django.db.models import QuerySet
from ..models import Bookmark, Verse

class BookmarkService:
    @staticmethod
    def get_bookmarks_by_user(user_id: int) -> QuerySet:
        """Get all bookmarks for a user."""
        return Bookmark.objects.filter(user_id=user_id).select_related('verse')
    
    @staticmethod
    def toggle_bookmark(user_id: int, verse_id: int) -> bool:
        """Toggle bookmark status for a verse."""
        bookmark, created = Bookmark.objects.get_or_create(
            user_id=user_id,
            verse_id=verse_id
        )
        if not created:
            bookmark.delete()
            return False
        return True
    
    @staticmethod
    def is_bookmarked(user_id: int, verse_id: int) -> bool:
        """Check if a verse is bookmarked by user."""
        return Bookmark.objects.filter(
            user_id=user_id,
            verse_id=verse_id
        ).exists()