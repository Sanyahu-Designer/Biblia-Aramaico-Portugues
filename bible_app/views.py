"""Main views for the Bible application."""
from django.shortcuts import render
from django.http import JsonResponse
from .models import Book, Chapter
from .services.bible_service import BibleService

def home(request):
    """Handle the home page view with Bible navigation."""
    bible_service = BibleService()
    books = bible_service.get_books()
    selected_book_id = request.GET.get('book')
    selected_chapter_id = request.GET.get('chapter')
    
    context = {
        'books': books,
        'selected_book_id': selected_book_id,
        'selected_chapter_id': selected_chapter_id,
    }
    
    if selected_book_id and selected_chapter_id:
        chapter_context = bible_service.get_chapter_context(int(selected_chapter_id))
        context.update(chapter_context)
    
    return render(request, 'bible_app/home.html', context)

def get_chapters(request):
    """API endpoint to get chapters for a specific book."""
    book_id = request.GET.get('book_id')
    if book_id:
        chapters = BibleService.get_chapters(book_id)
        return JsonResponse(list(chapters), safe=False)
    return JsonResponse({'error': 'Book ID is required'}, status=400)