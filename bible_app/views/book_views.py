"""Views for Book-related actions."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..services.book_service import BookService
from ..services.chapter_service import ChapterService

@login_required
def book_chapters(request, book_id):
    """Display chapters for a specific book."""
    book_service = BookService()
    chapter_service = ChapterService()
    
    book = book_service.get_book_by_id(book_id)
    chapters = chapter_service.get_chapters_by_book(book_id)
    
    context = {
        'book': book,
        'chapters': chapters,
    }
    return render(request, 'bible_app/book/chapters.html', context)

@login_required
def add_chapter(request, book_id):
    """Add a new chapter to a book."""
    book_service = BookService()
    chapter_service = ChapterService()
    
    book = book_service.get_book_by_id(book_id)
    
    if request.method == 'POST':
        try:
            number = int(request.POST.get('number'))
            chapter_service.create_chapter(book, number)
            messages.success(request, f'Capítulo {number} criado com sucesso!')
            return redirect('bible_app:book_chapters', book_id=book_id)
        except ValueError:
            messages.error(request, 'Número do capítulo inválido.')
        except Exception as e:
            messages.error(request, str(e))
    
    next_number = chapter_service.get_next_chapter_number(book_id)
    context = {
        'book': book,
        'next_number': next_number,
    }
    return render(request, 'bible_app/book/add_chapter.html', context)