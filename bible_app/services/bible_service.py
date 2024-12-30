"""Service for handling Bible navigation and retrieval operations."""
from django.db.models import QuerySet, Prefetch
from ..models import Book, Chapter, Verse

class BibleService:
    @staticmethod
    def get_books() -> QuerySet:
        """Get all books ordered by order field."""
        return Book.objects.all().order_by('order')

    @staticmethod
    def get_chapters(book_id: int) -> list:
        """Get all chapters for a specific book.
        
        Args:
            book_id (int): ID of the book
            
        Returns:
            list: List of chapters with their IDs and numbers
        """
        chapters = Chapter.objects.filter(book_id=book_id).order_by('number')
        return [{'id': chapter.id, 'number': chapter.number} for chapter in chapters]

    @staticmethod
    def get_chapter_context(chapter_id: int) -> dict:
        """Get complete chapter context including verses and navigation."""
        print(f"DEBUG - Getting context for chapter_id: {chapter_id}")
        
        try:
            # Get chapter with related book
            chapter = Chapter.objects.select_related('book').get(id=chapter_id)
            print(f"DEBUG - Found chapter: {chapter.number} from book {chapter.book.name}")
            
            # Debug verses using the new method
            verses = chapter.debug_verses()
            
            # Get navigation chapters
            prev_chapter = (Chapter.objects
                          .filter(book=chapter.book, number__lt=chapter.number)
                          .order_by('-number')
                          .first())
            
            next_chapter = (Chapter.objects
                          .filter(book=chapter.book, number__gt=chapter.number)
                          .order_by('number')
                          .first())
            
            # Convert QuerySet to list to ensure it's evaluated
            verses_list = list(verses.select_related('chapter', 'chapter__book').order_by('number'))
            
            context = {
                'chapter': chapter,
                'verses': verses_list,
                'previous_chapter': prev_chapter,
                'next_chapter': next_chapter
            }
            
            print("DEBUG - Final context verses count:", len(context['verses']))
            return context
            
        except Chapter.DoesNotExist:
            print(f"ERROR - Chapter {chapter_id} not found")
            return {
                'chapter': None,
                'verses': [],
                'previous_chapter': None,
                'next_chapter': None
            }
        except Exception as e:
            print(f"ERROR - Unexpected error in get_chapter_context: {str(e)}")
            return {
                'chapter': None,
                'verses': [],
                'previous_chapter': None,
                'next_chapter': None
            }

    @staticmethod
    def search_verses(query: str) -> list:
        """Busca versículos que contenham o texto especificado.
        
        Args:
            query (str): Texto a ser buscado
            
        Returns:
            list: Lista de resultados com título e texto
        """
        from django.db.models import Q
        
        if not query:
            return []

        verses = Verse.objects.filter(
            Q(aramaic_text__icontains=query) |  # Busca no texto aramaico
            Q(portuguese_text__icontains=query) |  # Busca no texto em português
            Q(chapter__book__name__icontains=query)  # Busca no nome do livro
        ).select_related('chapter', 'chapter__book')[:10]  # Limita a 10 resultados

        results = []
        for verse in verses:
            results.append({
                'url': f'/?book={verse.chapter.book.id}&chapter={verse.chapter.id}',
                'title': f'{verse.chapter.book.name} {verse.chapter.number}:{verse.number}',
                'text': verse.portuguese_text
            })
        
        return results