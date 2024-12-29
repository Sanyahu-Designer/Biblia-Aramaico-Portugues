# Generated by Django 5.1.2 on 2024-12-23 17:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0004_grammaticalcategory_aramaicword_gender_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Favoritado em')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary_app.aramaicword', verbose_name='Palavra')),
            ],
            options={
                'verbose_name': 'Palavra Favorita',
                'verbose_name_plural': 'Palavras Favoritas',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'word')},
            },
        ),
    ]
