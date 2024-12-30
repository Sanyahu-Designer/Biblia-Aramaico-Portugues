from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q, F
from .models import AramaicWord, WordCrossReference, GrammaticalCategory, WordOccurrence, Verse
from .services import WordOccurrenceService
from . import settings as dict_settings
import json

def home(request):
    """View para a página inicial do dicionário."""
    categories = GrammaticalCategory.objects.all()
    is_mobile = 'Mobile' in request.META.get('HTTP_USER_AGENT', '')
    items_per_page = dict_settings.ITEMS_PER_PAGE_MOBILE if is_mobile else dict_settings.ITEMS_PER_PAGE_DESKTOP
    initial_words = AramaicWord.objects.all().order_by('aramaic_word')[:items_per_page]
    
    return render(request, 'dictionary_app/home.html', {
        'categories': categories,
        'initial_words': initial_words,
        'items_per_page': items_per_page,
        'total_words': AramaicWord.objects.count()
    })

def search_words(request):
    """API para buscar palavras no dicionário."""
    try:
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        page = int(request.GET.get('page', 1))
        items_per_page = int(request.GET.get('items_per_page', dict_settings.ITEMS_PER_PAGE_DESKTOP))
        
        # Limita o número máximo de itens por página
        items_per_page = min(items_per_page, dict_settings.MAX_ITEMS_PER_LOAD)
        
        # Calcula o offset baseado na página
        offset = (page - 1) * items_per_page
        
        words = AramaicWord.objects.all()
        total_words = words.count()
        
        if query:
            words = words.filter(
                Q(aramaic_word__icontains=query) |
                Q(transliteration__icontains=query) |
                Q(portuguese_translation__icontains=query)
            )
        
        if category:
            words = words.filter(grammatical_category_id=category)
        
        # Obtém o total de resultados para esta busca
        total_filtered = words.count()
        
        # Ordena e pagina os resultados
        words = words.order_by('aramaic_word')[offset:offset + items_per_page]
        
        # Verifica se há mais resultados
        has_more = (offset + items_per_page) < total_filtered
        
        return JsonResponse({
            'words': [{
                'id': word.id,
                'aramaic_word': word.aramaic_word,
                'transliteration': word.transliteration,
                'portuguese_translation': word.portuguese_translation,
                'grammatical_category': word.grammatical_category.name if word.grammatical_category else None
            } for word in words],
            'total': total_filtered,
            'has_more': has_more,
            'current_page': page
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def word_details(request, word_id):
    """Retorna detalhes de uma palavra para o offcanvas."""
    word = get_object_or_404(AramaicWord, id=word_id)
    
    # Detecta ocorrências usando o serviço
    occurrences = WordOccurrenceService.detect_word_occurrences(word.aramaic_word)
    
    # Obtém referências cruzadas
    references = WordCrossReference.objects.filter(word=word)
    reference_data = [{'context': ref.context} for ref in references]
    
    data = {
        'id': word.id,
        'aramaic_word': word.aramaic_word,
        'transliteration': word.transliteration,
        'portuguese_translation': word.portuguese_translation,
        'grammatical_category': word.grammatical_category.name if word.grammatical_category else None,
        'root_word': word.root_word,
        'gender': word.get_gender_display() if word.gender else None,
        'number': word.get_number_display() if word.number else None,
        'notes': word.notes,
        'references': reference_data,
        'occurrences': occurrences['occurrences'],
        'total_occurrences': occurrences['total']
    }
    
    return JsonResponse(data)

@require_http_methods(["GET"])
def detect_occurrences(request):
    """API para detectar ocorrências de uma palavra."""
    word = request.GET.get('word', '')
    if not word:
        return JsonResponse({'error': 'Palavra não fornecida'}, status=400)
        
    occurrences = WordOccurrenceService.detect_occurrences(word)
    return JsonResponse(occurrences)

def edit_word(request, word_id=None):
    """View para adicionar ou editar uma palavra."""
    if word_id:
        word = get_object_or_404(AramaicWord, id=word_id)
        title = f'Editar {word.aramaic_word}'
    else:
        word = None
        title = 'Nova Palavra'
    
    if request.method == 'POST':
        # Processar o formulário
        data = request.POST
        detected_occurrences = json.loads(data.get('detected_occurrences', '[]'))
        
        # Criar ou atualizar palavra
        if word_id:
            # Atualizar palavra existente
            word.aramaic_word = data['aramaic_word']
            word.transliteration = data['transliteration']
            word.portuguese_translation = data['portuguese_translation']
            word.grammatical_category_id = data['grammatical_category'] or None
            word.root_word = data['root_word'] or None
            word.gender = data['gender'] or None
            word.number = data['number'] or None
            word.notes = data['notes'] or None
            word.save()
        else:
            # Criar nova palavra
            word = AramaicWord.objects.create(
                aramaic_word=data['aramaic_word'],
                transliteration=data['transliteration'],
                portuguese_translation=data['portuguese_translation'],
                grammatical_category_id=data['grammatical_category'] or None,
                root_word=data['root_word'] or None,
                gender=data['gender'] or None,
                number=data['number'] or None,
                notes=data['notes'] or None
            )
        
        # Processar ocorrências detectadas
        if detected_occurrences:
            # Primeiro remove ocorrências existentes
            WordOccurrence.objects.filter(word=word).delete()
            
            # Adiciona novas ocorrências
            for occ in detected_occurrences:
                try:
                    verse = Verse.objects.get(
                        chapter__book__name=occ['book'],
                        chapter__number=occ['chapter'],
                        number=occ['verse']
                    )
                    WordOccurrence.objects.create(word=word, verse=verse)
                except Verse.DoesNotExist:
                    continue
        
        # Processar referências cruzadas
        if 'references' in data:
            references = json.loads(data['references'])
            # Remove referências existentes
            WordCrossReference.objects.filter(word=word).delete()
            
            # Adiciona novas referências
            for ref in references:
                try:
                    reference_word = AramaicWord.objects.get(id=ref['id'])
                    WordCrossReference.objects.create(
                        word=word,
                        reference_word=reference_word,
                        context=ref.get('context', '')
                    )
                except AramaicWord.DoesNotExist:
                    continue
        
        return redirect('dictionary:home')
    
    # GET request
    context = {
        'word': word,
        'title': title,
        'categories': GrammaticalCategory.objects.all(),
        'gender_choices': AramaicWord.GENDER_CHOICES,
        'number_choices': AramaicWord.NUMBER_CHOICES,
        'available_words': AramaicWord.objects.exclude(id=word_id if word_id else None).order_by('aramaic_word')
    }
    
    return render(request, 'dictionary_app/word_form.html', context)

@login_required
@require_http_methods(["POST"])
def toggle_favorite(request):
    return JsonResponse({
        'status': 'success',
        'is_favorite': False
    })
