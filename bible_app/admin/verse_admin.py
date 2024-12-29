"""Admin configuration for Verse model."""
from django.contrib import admin
from django.utils.html import format_html
from ..models import Verse

class VerseAdmin(admin.ModelAdmin):
    list_display = ('reference', 'aramaic_preview', 'portuguese_preview', 'translator')
    list_filter = ('chapter__book', 'chapter', 'translator')
    search_fields = ('aramaic_text', 'portuguese_text', 'translator_note')
    ordering = ('chapter__book__order', 'chapter__number', 'number')
    
    def reference(self, obj):
        return f'{obj.chapter.book.name} {obj.chapter.number}:{obj.number}'
    reference.short_description = 'Referência'
    
    def aramaic_preview(self, obj):
        return format_html('<div dir="rtl" style="font-family: \'SBL Hebrew\', serif;">{}</div>',
                         obj.aramaic_text[:100] + '...' if len(obj.aramaic_text) > 100 else obj.aramaic_text)
    aramaic_preview.short_description = 'Texto Aramaico'
    
    def portuguese_preview(self, obj):
        return obj.portuguese_text[:100] + '...' if len(obj.portuguese_text) > 100 else obj.portuguese_text
    portuguese_preview.short_description = 'Texto Português'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('chapter', 'chapter__book')