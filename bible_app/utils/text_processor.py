"""Utility for processing text and adding tooltips."""
import re
from typing import Dict
from django.utils.html import escape
from ..models.traducao_especifica import TraducaoEspecifica

class TextProcessor:
    def __init__(self):
        self._traducoes_cache = None
        self._cache_timestamp = None

    @property
    def traducoes(self) -> Dict[str, str]:
        """Get translations dictionary with cache."""
        from django.utils import timezone
        now = timezone.now()
        
        # Refresh cache every hour
        if (not self._traducoes_cache or 
            not self._cache_timestamp or 
            (now - self._cache_timestamp).seconds > 3600):
            
            self._traducoes_cache = {
                t.termo_original.lower(): t.traducao 
                for t in TraducaoEspecifica.objects.all()
            }
            self._cache_timestamp = now
        
        return self._traducoes_cache

    def processar_tooltips(self, texto: str) -> str:
        """Process text and add tooltips for known translations.
        
        Args:
            texto: Original text to process
            
        Returns:
            str: Processed text with tooltip spans
        """
        if not texto:
            return texto

        # Escape HTML first
        texto = escape(texto)
        
        # Split text into words while preserving spaces and punctuation
        palavras = re.findall(r'\S+|\s+', texto)
        resultado = []
        
        for palavra in palavras:
            if palavra.isspace():
                resultado.append(palavra)
                continue
                
            termo_limpo = palavra.strip('.,!?:;').lower()
            
            if termo_limpo in self.traducoes:
                traducao = self.traducoes[termo_limpo]
                resultado.append(
                    f'<span class="tooltip-word" data-tooltip="{escape(traducao)}">{palavra}</span>'
                )
            else:
                resultado.append(palavra)
        
        return ''.join(resultado)

text_processor = TextProcessor()