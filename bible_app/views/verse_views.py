"""Views for Verse-related actions."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Verse
from ..services.verse_service import VerseService

@login_required
def verse_detail(request, verse_id):
    """Display details for a specific verse."""
    verse = get_object_or_404(Verse, id=verse_id)
    context = {
        'verse': verse,
    }
    return render(request, 'bible_app/verse/detail.html', context)

@login_required
def edit_verse(request, verse_id):
    """Edit an existing verse."""
    verse = get_object_or_404(Verse, id=verse_id)
    verse_service = VerseService()
    
    if request.method == 'POST':
        try:
            verse_data = {
                'number': int(request.POST.get('number')),
                'aramaic_text': request.POST.get('aramaic_text'),
                'portuguese_text': request.POST.get('portuguese_text'),
            }
            verse_service.update_verse(verse, **verse_data)
            messages.success(request, 'Versículo atualizado com sucesso!')
            return redirect('bible_app:verse_detail', verse_id=verse_id)
        except ValueError:
            messages.error(request, 'Dados inválidos.')
        except Exception as e:
            messages.error(request, str(e))
    
    context = {
        'verse': verse,
    }
    return render(request, 'bible_app/verse/edit.html', context)