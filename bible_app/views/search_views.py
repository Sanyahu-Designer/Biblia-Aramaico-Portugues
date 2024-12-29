from django.http import JsonResponse
from django.urls import reverse
from ..services.verse_service import VerseService
from ..services.book_service import BookService
from ..services.chapter_service import ChapterService

def search_content(request):
    """
    Endpoint para busca unificada de conteúdo (livros, capítulos e versículos)
    """
    query = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)
    
    if not query:
        return JsonResponse({'results': []})

    try:
        page = int(page)
    except ValueError:
        page = 1

    results = []
    
    # Busca versículos
    verses = VerseService.search_verses(query, page)
    for verse in verses:
        # Construir a URL usando o livro, capítulo e versículo
        url = f"/?book={verse.chapter.book.id}&chapter={verse.chapter.number}&verse={verse.number}"
        results.append({
            'type': 'verse',
            'id': verse.id,
            'title': f'{verse.chapter.book.name} {verse.chapter.number}:{verse.number}',
            'text': verse.portuguese_text[:100] + '...' if len(verse.portuguese_text) > 100 else verse.portuguese_text,
            'url': url
        })

    return JsonResponse({'results': results})
