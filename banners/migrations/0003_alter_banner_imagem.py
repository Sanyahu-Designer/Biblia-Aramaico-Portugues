# Generated by Django 5.1.2 on 2024-12-25 05:41

import banners.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_remove_banner_conteudo_remove_banner_titulo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='imagem',
            field=models.ImageField(help_text='Faça upload da arte do banner no formato Instagram Story (1080x1920 pixels)', upload_to='banners/', validators=[banners.models.validate_image_dimensions], verbose_name='Imagem'),
        ),
    ]
