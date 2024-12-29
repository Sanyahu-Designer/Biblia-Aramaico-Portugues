"""Views for Chapter-related actions."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Chapter
from ..services.verse_service import VerseService

@login_required
def chapter_verses(request, chapter_id):
    """Display verses for a specific chapter."""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    verse_service = VerseService()
    verses = verse_service.get_verses_by_chapter(chapter_id)
    
    # Get previous and next chapters
    previous_chapter = Chapter.objects.filter(
        book=chapter.book,
        number__lt=chapter.number
    ).order_by('-number').first()
    
    next_chapter = Chapter.objects.filter(
        book=chapter.book,
        number__gt=chapter.number
    ).order_by('number').first()
    
    context = {
        'chapter': chapter,
        'verses': verses,
        'previous_chapter': previous_chapter,
        'next_chapter': next_chapter,
    }
    return render(request, 'bible_app/chapter/verses.html', context)

@login_required
def add_verse(request, chapter_id):
    """Add a new verse to a chapter."""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    verse_service = VerseService()
    
    if request.method == 'POST':
        try:
            verse_data = {
                'chapter': chapter,
                'number': int(request.POST.get('number')),
                'aramaic_text': request.POST.get('aramaic_text'),
                'portuguese_text': request.POST.get('portuguese_text'),
            }
            verse_service.create_verse(**verse_data)
            messages.success(request, f'Versículo {verse_data["number"]} criado com sucesso!')
            return redirect('bible_app:chapter_verses', chapter_id=chapter_id)
        except ValueError:
            messages.error(request, 'Dados inválidos.')
        except Exception as e:
            messages.error(request, str(e))
    
    next_number = verse_service.get_next_verse_number(chapter_id)
    context = {
        'chapter': chapter,
        'next_number': next_number,
    }
    return render(request, 'bible_app/chapter/add_verse.html', context)