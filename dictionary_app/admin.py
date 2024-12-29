from django.contrib import admin
from django import forms
from django.db import connection
from .models import GrammaticalCategory, AramaicWord, WordOccurrence, WordCrossReference

@admin.register(GrammaticalCategory)
class GrammaticalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

class WordOccurrenceInline(admin.TabularInline):
    model = WordOccurrence
    extra = 0
    readonly_fields = ['verse']
    can_delete = False

class WordCrossReferenceInline(admin.StackedInline):
    model = WordCrossReference
    extra = 1
    fields = ['context']
    verbose_name = 'Referência Cruzada'
    verbose_name_plural = 'Referências Cruzadas'

@admin.register(AramaicWord)
class AramaicWordAdmin(admin.ModelAdmin):
    list_display = ['aramaic_word', 'transliteration', 'portuguese_translation', 'grammatical_category']
    search_fields = ['aramaic_word', 'transliteration', 'portuguese_translation']
    list_filter = ['grammatical_category', 'gender', 'number']
    inlines = [WordCrossReferenceInline, WordOccurrenceInline]
    fields = [
        'aramaic_word', 'transliteration', 'portuguese_translation',
        'grammatical_category', 'root_word', 'gender', 'number',
        'notes'
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "grammatical_category":
            kwargs["widget"] = forms.Select(attrs={'class': 'select-only'})
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Ao salvar a palavra, detecta automaticamente as ocorrências."""
        # Primeiro salvamos o objeto para garantir que ele exista no banco
        super().save_model(request, obj, form, change)
        
        # Se for uma nova palavra ou o texto em aramaico foi alterado
        if not change or form.changed_data and 'aramaic_word' in form.changed_data:
            from .services import WordOccurrenceService
            from bible_app.models import Verse
            from django.db import transaction
            
            try:
                with transaction.atomic():
                    # Remove todas as ocorrências antigas
                    WordOccurrence.objects.filter(word=obj).delete()
                    
                    # Detecta e salva novas ocorrências
                    results = WordOccurrenceService.detect_word_occurrences(obj.aramaic_word)
                    for occ in results['occurrences']:
                        try:
                            verse = Verse.objects.get(
                                chapter__book__name=occ['book'],
                                chapter__number=occ['chapter'],
                                number=occ['verse']
                            )
                            # Verifica se já existe uma ocorrência antes de criar
                            WordOccurrence.objects.get_or_create(
                                word=obj,
                                verse=verse
                            )
                        except Verse.DoesNotExist:
                            continue
            except Exception as e:
                # Se houver algum erro, tenta limpar todas as ocorrências
                WordOccurrence.objects.filter(word=obj).delete()
                raise e
