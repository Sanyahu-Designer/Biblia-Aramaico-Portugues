"""Service for handling user notes."""
from django.db.models import QuerySet
from ..models import UserNote, Verse

class NoteService:
    @staticmethod
    def get_notes_by_user_and_verse(user_id: int, verse_id: int) -> QuerySet:
        """Get notes for a specific user and verse."""
        return UserNote.objects.filter(user_id=user_id, verse_id=verse_id)
    
    @staticmethod
    def create_note(user_id: int, verse_id: int, text: str) -> UserNote:
        """Create a new note."""
        return UserNote.objects.create(
            user_id=user_id,
            verse_id=verse_id,
            text=text
        )
    
    @staticmethod
    def update_note(note_id: int, text: str) -> UserNote:
        """Update an existing note."""
        note = UserNote.objects.get(id=note_id)
        note.text = text
        note.save()
        return note
    
    @staticmethod
    def delete_note(note_id: int) -> None:
        """Delete a note."""
        UserNote.objects.filter(id=note_id).delete()