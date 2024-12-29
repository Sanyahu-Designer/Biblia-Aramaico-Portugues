"""Admin configuration for Chapter model."""
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.html import format_html
from ..models import Chapter
from ..services.verse_service import VerseService

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'number', 'verse_count', 'verses_link')
    list_filter = ('book',)
    search_fields = ('book__name', 'number')
    ordering = ('book__order', 'number')
    
    def verse_count(self, obj):
        return obj.verses.count()
    verse_count.short_description = 'Número de Versículos'
    
    def verses_link(self, obj):
        url = reverse('admin:chapter_verses', args=[obj.pk])
        return format_html('<a href="{}">Ver Versículos</a>', url)
    verses_link.short_description = 'Versículos'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:chapter_id>/verses/',
                 self.admin_site.admin_view(self.verse_list_view),
                 name='chapter_verses'),
            path('<int:chapter_id>/verses/add/',
                 self.admin_site.admin_view(self.add_verse_view),
                 name='add_verse'),
        ]
        return custom_urls + urls
    
    def verse_list_view(self, request, chapter_id):
        chapter = get_object_or_404(Chapter, id=chapter_id)
        verse_service = VerseService()
        verses = verse_service.get_verses_by_chapter(chapter_id)
        
        context = {
            **self.admin_site.each_context(request),
            'chapter': chapter,
            'verses': verses,
            'opts': self.model._meta,
            'has_add_permission': self.has_add_permission(request),
            'title': f'{chapter.book.name} - Capítulo {chapter.number} - Versículos',
            'app_label': 'bible_app',
            'original': chapter,
        }
        return render(request, 'admin/bible_app/chapter/verse_list.html', context)
    
    def add_verse_view(self, request, chapter_id):
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
                return redirect('admin:chapter_verses', chapter_id=chapter_id)
            except ValueError:
                messages.error(request, 'Dados inválidos.')
            except Exception as e:
                messages.error(request, str(e))
        
        next_number = verse_service.get_next_verse_number(chapter_id)
        context = {
            **self.admin_site.each_context(request),
            'chapter': chapter,
            'next_number': next_number,
            'opts': self.model._meta,
            'title': f'Adicionar Versículo - {chapter.book.name} {chapter.number}',
            'app_label': 'bible_app',
            'original': chapter,
        }
        return render(request, 'admin/bible_app/chapter/add_verse.html', context)