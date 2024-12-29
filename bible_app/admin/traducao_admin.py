"""Admin configuration for TraducaoEspecifica model."""
from django.contrib import admin
from django.utils.html import format_html
from ..models.traducao_especifica import TraducaoEspecifica
from ..utils.text_processor import text_processor

class TraducaoEspecificaAdmin(admin.ModelAdmin):
    list_display = ('termo_original', 'traducao', 'preview', 'created_at')
    search_fields = ('termo_original', 'traducao', 'notas')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('termo_original',)
    
    fieldsets = (
        (None, {
            'fields': ('termo_original', 'traducao')
        }),
        ('Informações Adicionais', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def preview(self, obj):
        """Show how the term will appear with tooltip."""
        processed = text_processor.processar_tooltips(obj.termo_original)
        return format_html(
            '<div style="min-width:200px">{}</div>',
            processed
        )
    preview.short_description = 'Visualização'
    
    def save_model(self, request, obj, form, change):
        """Clear text processor cache when translation is saved."""
        super().save_model(request, obj, form, change)
        text_processor._traducoes_cache = None
        
    class Media:
        css = {
            'all': ('css/tooltip.css',)
        }