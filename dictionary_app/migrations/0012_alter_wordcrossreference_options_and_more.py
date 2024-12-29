# Generated by Django 5.1.2 on 2024-12-24 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bible_app', '__first__'),
        ('dictionary_app', '0011_alter_aramaicword_aramaic_word_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wordcrossreference',
            options={'verbose_name': 'Referência Cruzada', 'verbose_name_plural': 'Referências Cruzadas'},
        ),
        migrations.RemoveField(
            model_name='wordcrossreference',
            name='reference_location',
        ),
        migrations.RemoveField(
            model_name='wordcrossreference',
            name='reference_text',
        ),
        migrations.AddField(
            model_name='wordcrossreference',
            name='reference_word',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referenced_by', to='dictionary_app.aramaicword', verbose_name='Palavra de Referência'),
        ),
        migrations.AlterField(
            model_name='wordcrossreference',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references', to='dictionary_app.aramaicword', verbose_name='Palavra'),
        ),
        migrations.CreateModel(
            name='WordOccurrence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('verse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible_app.verse', verbose_name='Versículo')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='occurrences', to='dictionary_app.aramaicword', verbose_name='Palavra')),
            ],
            options={
                'verbose_name': 'Ocorrência',
                'verbose_name_plural': 'Ocorrências',
                'unique_together': {('word', 'verse')},
            },
        ),
        migrations.DeleteModel(
            name='WordVerse',
        ),
    ]
