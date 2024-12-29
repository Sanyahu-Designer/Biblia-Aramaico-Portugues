"""Admin configuration for Book model."""
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.html import format_html
from ..models import Book
from ..services.book_service import BookService
from ..services.chapter_service import ChapterService

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'chapter_count', 'chapters_link')
    search_fields = ('name',)
    ordering = ('order',)
    
    def chapter_count(self, obj):
        return obj.chapters.count()
    chapter_count.short_description = 'Número de Capítulos'
    
    def chapters_link(self, obj):
        url = reverse('admin:book_chapters', args=[obj.pk])
        return format_html('<a href="{}">Ver Capítulos</a>', url)
    chapters_link.short_description = 'Capítulos'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:book_id>/chapters/',
                 self.admin_site.admin_view(self.chapter_list_view),
                 name='book_chapters'),
            path('<int:book_id>/chapters/add/',
                 self.admin_site.admin_view(self.add_chapter_view),
                 name='add_chapter'),
        ]
        return custom_urls + urls
    
    def chapter_list_view(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        chapter_service = ChapterService()
        chapters = chapter_service.get_chapters_by_book(book_id)
        
        context = {
            **self.admin_site.each_context(request),
            'book': book,
            'chapters': chapters,
            'opts': self.model._meta,
            'has_add_permission': self.has_add_permission(request),
            'title': f'Capítulos - {book.name}',
            'app_label': 'bible_app',
            'original': book,
        }
        return render(request, 'admin/bible_app/book/chapter_list.html', context)
    
    def add_chapter_view(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        chapter_service = ChapterService()
        
        if request.method == 'POST':
            try:
                number = int(request.POST.get('number'))
                chapter_service.create_chapter(book, number)
                messages.success(request, f'Capítulo {number} criado com sucesso!')
                return redirect('admin:book_chapters', book_id=book_id)
            except ValueError:
                messages.error(request, 'Número do capítulo inválido.')
            except Exception as e:
                messages.error(request, str(e))
        
        next_number = chapter_service.get_next_chapter_number(book_id)
        context = {
            **self.admin_site.each_context(request),
            'book': book,
            'next_number': next_number,
            'opts': self.model._meta,
            'title': f'Adicionar Capítulo - {book.name}',
            'app_label': 'bible_app',
            'original': book,
        }
        return render(request, 'admin/bible_app/book/add_chapter.html', context)