from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from .models import Banner
import json
import logging
import requests
from urllib.parse import urlparse
import os

logger = logging.getLogger(__name__)

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_next_banner(request):
    try:
        # Chave de cache única para cada sessão
        session_id = request.session.session_key or 'default'
        cache_key = f'active_banner_{session_id}'
        last_banner_key = f'last_banner_{session_id}'
        
        # Pega o ID do último banner mostrado
        last_banner_id = cache.get(last_banner_key)
        
        # Busca todos os banners ativos
        now = timezone.now()
        banners = Banner.objects.filter(
            ativo=True,
            data_inicio__lte=now,
            data_fim__gte=now
        ).order_by('-prioridade')
        
        if not banners.exists():
            return JsonResponse({'error': 'Nenhum banner disponível'}, status=404)
        
        # Se houver mais de um banner, exclui o último mostrado
        if banners.count() > 1 and last_banner_id:
            banners = banners.exclude(id=last_banner_id)
        
        # Seleciona um banner aleatório
        banner = banners.order_by('?').first()
        
        if banner:
            # Salva o ID do banner atual como último mostrado
            cache.set(last_banner_key, banner.id, timeout=300)  # 5 minutos
            
            # Incrementa visualização
            banner.incrementar_visualizacao()
            
            # Prepara os dados do banner
            banner_data = {
                'id': banner.id,
                'imagem': f"{settings.SITE_URL}{settings.MEDIA_URL}banners/{os.path.basename(banner.imagem.name)}",
                'link': banner.link,
                'posicao': banner.posicao
            }
            
            # Cache dos dados do banner
            cache.set(cache_key, banner_data, timeout=300)  # 5 minutos
            return JsonResponse(banner_data)
            
        return JsonResponse({'error': 'Nenhum banner disponível'}, status=404)
            
    except Exception as e:
        logger.error(f'Error in get_next_banner: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)

@csrf_protect
@require_http_methods(["POST"])
def register_click(request, banner_id):
    try:
        banner = Banner.objects.get(id=banner_id)
        banner.incrementar_clicks()
        return JsonResponse({'success': True})
    except Banner.DoesNotExist:
        return JsonResponse({'error': 'Banner not found'}, status=404)
    except Exception as e:
        logger.error(f'Error in register_click: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)

def serve_banner_image(request, filename):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, 'banners', filename)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='image/webp')
        raise Http404("Imagem não encontrada")
    except Exception as e:
        logger.error(f"Erro ao servir imagem do banner: {e}")
        raise Http404("Erro ao servir imagem")
