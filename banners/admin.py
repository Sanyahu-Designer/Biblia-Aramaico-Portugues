from django.contrib import admin
from .models import Banner

# Register your models here.

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_cliente', 'data_inicio', 'data_fim', 'valor_pago', 'prioridade', 'visualizacoes', 'clicks', 'ativo']
    list_filter = ['ativo', 'posicao']
    readonly_fields = ['visualizacoes', 'clicks']
    
    fieldsets = (
        ('Banner', {
            'fields': ('nome_cliente', 'imagem', 'link')
        }),
        ('Configurações', {
            'fields': ('posicao', 'prioridade', 'ativo')
        }),
        ('Período e Valor', {
            'fields': ('data_inicio', 'data_fim', 'valor_pago')
        }),
        ('Estatísticas', {
            'fields': ('visualizacoes', 'clicks'),
            'classes': ('collapse',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.readonly_fields
        return []  # Adding new
