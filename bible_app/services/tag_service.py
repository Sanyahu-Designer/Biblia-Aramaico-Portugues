"""Service for handling verse tags."""
from django.db.models import QuerySet
from ..models import Tag, VerseTag

class TagService:
    @staticmethod
    def get_tags_by_verse(verse_id: int) -> QuerySet:
        """Get all tags for a verse."""
        return Tag.objects.filter(versetag__verse_id=verse_id)
    
    @staticmethod
    def add_tag_to_verse(user_id: int, verse_id: int, tag_name: str) -> VerseTag:
        """Add a tag to a verse."""
        tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
        verse_tag, _ = VerseTag.objects.get_or_create(
            user_id=user_id,
            verse_id=verse_id,
            tag=tag
        )
        return verse_tag
    
    @staticmethod
    def remove_tag_from_verse(user_id: int, verse_id: int, tag_id: int) -> None:
        """Remove a tag from a verse."""
        VerseTag.objects.filter(
            user_id=user_id,
            verse_id=verse_id,
            tag_id=tag_id
        ).delete()