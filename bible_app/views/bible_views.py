from django.shortcuts import render
from django.http import JsonResponse
from bible_app.services.bible_service import BibleService
from bible_app.services.chapter_service import ChapterService
from bible_app.services.preferences_service import PreferencesService
from bible_app.models import Chapter, Verse

def get_chapters(request):
    """API endpoint to get chapters for a specific book."""
    book_id = request.GET.get('book_id')
    if not book_id:
        return JsonResponse({'error': 'Book ID is required'}, status=400)
    
    bible_service = BibleService()
    try:
        chapters = bible_service.get_chapters(book_id)
        return JsonResponse(chapters, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def search(request):
    """API endpoint para buscar versículos."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})
    
    bible_service = BibleService()
    results = bible_service.search_verses(query)
    return JsonResponse({'results': results})

def home(request):
    """Handle the home page view with Bible navigation."""
    bible_service = BibleService()
    chapter_service = ChapterService()
    preferences_service = PreferencesService()
    
    print("DEBUG - Request params:", request.GET)
    
    selected_book_id = request.GET.get('book')
    selected_chapter_id = request.GET.get('chapter')
    selected_verse = request.GET.get('verse')  # Novo parâmetro
    
    print("DEBUG - Selected book:", selected_book_id)
    print("DEBUG - Selected chapter:", selected_chapter_id)
    print("DEBUG - Selected verse:", selected_verse)
    
    context = {
        'books': bible_service.get_books(),
        'selected_book_id': selected_book_id,
        'selected_chapter_id': selected_chapter_id,
        'user_preferences': {},
        'verses': [],
        'previous_chapter': None,
        'next_chapter': None
    }
    
    if request.user.is_authenticated:
        try:
            context['user_preferences'] = preferences_service.get_user_preferences(request.user.id)
        except Exception as e:
            print(f"Error getting user preferences: {e}")
    
    if selected_book_id and selected_chapter_id:
        try:
            # Se vier da busca (tem versículo), usa o número do capítulo
            if selected_verse:
                chapter = Chapter.objects.get(
                    book_id=selected_book_id,
                    number=selected_chapter_id
                )
            else:
                # Se for navegação normal, usa o ID do capítulo
                chapter = Chapter.objects.get(
                    id=selected_chapter_id,
                    book_id=selected_book_id
                )
            
            print(f"DEBUG - Loading verses for chapter {chapter}")
            
            # Base query
            verses_query = Verse.objects.select_related('chapter', 'chapter__book')
            
            # Se tiver um versículo específico da busca, mostrar apenas ele
            if selected_verse:
                verses_query = verses_query.filter(
                    chapter=chapter,
                    number=selected_verse
                )
            else:
                # Caso contrário, mostrar todos os versículos do capítulo
                verses_query = verses_query.filter(
                    chapter=chapter
                )
            
            verses_list = list(verses_query.order_by('number'))
            print(f"DEBUG - Found {len(verses_list)} verses")
            
            if verses_list:
                print(f"DEBUG - First verse: {verses_list[0].aramaic_text[:100]}")
            
            context.update({
                'chapter': chapter,
                'verses': verses_list,
                'previous_chapter': Chapter.objects.filter(
                    book_id=selected_book_id,
                    number__lt=chapter.number
                ).order_by('-number').first(),
                'next_chapter': Chapter.objects.filter(
                    book_id=selected_book_id,
                    number__gt=chapter.number
                ).order_by('number').first()
            })
            
            print("DEBUG - Context updated with verses")
            
        except Chapter.DoesNotExist:
            print(f"Error: Chapter {selected_chapter_id} not found")
        except Exception as e:
            print(f"Error loading verses: {str(e)}")
    
    return render(request, 'bible_app/home.html', context)