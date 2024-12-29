from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q, F
from .models import AramaicWord, WordCrossReference, GrammaticalCategory, WordOccurrence, Verse
from .services import WordOccurrenceService
import json

def home(request):
    """View para a página inicial do dicionário."""
    categories = GrammaticalCategory.objects.all()
    return render(request, 'dictionary_app/home.html', {'categories': categories})

def search_words(request):
    """API para buscar palavras no dicionário."""
    try:
        print("=== Início da busca de palavras ===")
        print(f"Método da requisição: {request.method}")
        print(f"Usuário autenticado: {request.user.is_authenticated}")
        print(f"GET params: {request.GET}")
        
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        
        print(f"Query: '{query}', Category: '{category}'")
        
        words = AramaicWord.objects.all()
        total_words = words.count()
        print(f"Total de palavras no banco: {total_words}")
        
        if query:
            words = words.filter(
                Q(aramaic_word__icontains=query) |
                Q(transliteration__icontains=query) |
                Q(portuguese_translation__icontains=query)
            )
            print(f"Após filtro de query: {words.count()} palavras")
        
        if category:
            words = words.filter(grammatical_category_id=category)
            print(f"Após filtro de categoria: {words.count()} palavras")
        
        results = []
        words_list = list(words[:50])  # Limitando a 50 resultados
        print(f"Processando {len(words_list)} palavras")
        
        for word in words_list:
            # Verifica favoritos apenas se o usuário estiver autenticado
            is_favorite = False
            if request.user.is_authenticated:
                is_favorite = word.favorites.filter(id=request.user.id).exists()
            
            word_data = {
                'id': word.id,
                'aramaic_word': word.aramaic_word,
                'transliteration': word.transliteration,
                'portuguese_translation': word.portuguese_translation,
                'category': word.grammatical_category.name if word.grammatical_category else None,
                'is_favorite': is_favorite
            }
            results.append(word_data)
            print(f"Processada palavra: {word.aramaic_word}")
        
        print(f"Total de resultados: {len(results)}")
        print("=== Fim da busca de palavras ===")
        return JsonResponse({'words': results})
    except Exception as e:
        print(f"!!! ERRO ao buscar palavras: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)

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
