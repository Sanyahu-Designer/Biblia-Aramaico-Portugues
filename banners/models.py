from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from PIL import Image
import os
import logging
from django.conf import settings

# Create your models here.

logger = logging.getLogger(__name__)

def validate_image_dimensions(image):
    if not image:
        return
    
    # Verifica o formato do arquivo
    valid_formats = ['image/jpeg', 'image/png', 'image/webp']
    if hasattr(image.file, 'content_type') and image.file.content_type not in valid_formats:
        raise ValidationError('Formato de arquivo inválido. Use JPEG, PNG ou WEBP.')
    
    # Abre a imagem usando PIL
    try:
        img = Image.open(image)
        width, height = img.size
        
        # Dimensões do banner (540x960)
        required_width = 540
        required_height = 960
        
        if width != required_width or height != required_height:
            raise ValidationError(
                f'A imagem deve ter exatamente {required_width}x{required_height} pixels (formato 9:16). '
                f'A imagem enviada tem {width}x{height} pixels.'
            )
    except Exception as e:
        raise ValidationError(f'Erro ao processar imagem: {str(e)}')

class Banner(models.Model):
    nome_cliente = models.CharField('Nome do Cliente', max_length=200, help_text='Nome do cliente do banner', null=True, blank=True)
    imagem = models.ImageField(
        'Imagem', 
        upload_to='banners/', 
        help_text='Faça upload da arte do banner no formato 9:16 (540x960 pixels). Use JPEG, PNG ou WEBP.',
        validators=[validate_image_dimensions]
    )
    link = models.URLField('Link', blank=True, help_text='Link para onde o banner irá direcionar quando clicado')
    data_inicio = models.DateTimeField('Data de Início')
    data_fim = models.DateTimeField('Data de Término')
    valor_pago = models.DecimalField('Valor Pago', max_digits=10, decimal_places=2)
    prioridade = models.IntegerField('Prioridade', default=0)
    clicks = models.IntegerField('Clicks', default=0)
    visualizacoes = models.IntegerField('Visualizações', default=0)
    posicao = models.CharField('Posição', max_length=10, choices=[
        ('left', 'Esquerda'),
        ('right', 'Direita')
    ], default='right')
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['-prioridade', 'data_inicio']

    def __str__(self):
        return f'Banner {self.id} - {self.data_inicio.strftime("%d/%m/%Y")}'

    @classmethod
    def get_next_banner(cls):
        try:
            now = timezone.now()
            banner = cls.objects.filter(
                ativo=True,
                data_inicio__lte=now,
                data_fim__gte=now
            ).order_by('-prioridade', '?').first()
            
            if banner:
                banner.incrementar_visualizacao()
            return banner
        except Exception as e:
            logger.error(f'Erro ao buscar próximo banner: {e}')
            return None

    def incrementar_visualizacao(self):
        from django.db.models import F
        Banner.objects.filter(id=self.id).update(visualizacoes=F('visualizacoes') + 1)
        self.refresh_from_db()

    def incrementar_clicks(self):
        self.clicks += 1
        self.save()

    def incrementar_visualizacoes(self):
        self.visualizacoes += 1
        self.save()

    def get_image_url(self):
        if settings.DEBUG:
            return f"{settings.MEDIA_URL}banners/{self.imagem.name.split('/')[-1]}"
        return f"https://staging.sanyahudesigner.com.br/media/banners/{self.imagem.name.split('/')[-1]}"

    def to_dict(self):
        return {
            'id': self.id,
            'imagem': self.get_image_url(),
            'link': self.link,
            'posicao': self.posicao
        }

    def delete(self, *args, **kwargs):
        # Guarda o caminho do arquivo
        storage = self.imagem.storage
        path = self.imagem.path
        
        # Deleta o registro do banco
        super().delete(*args, **kwargs)
        
        # Remove o arquivo físico
        if storage.exists(path):
            storage.delete(path)
