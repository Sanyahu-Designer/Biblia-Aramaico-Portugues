from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('abbreviation', models.CharField(max_length=10, verbose_name='Abreviação')),
                ('order', models.IntegerField(verbose_name='Ordem')),
            ],
            options={
                'verbose_name': 'Livro',
                'verbose_name_plural': 'Livros',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Número')),
                ('book', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='chapters', to='bible_app.book', verbose_name='Livro')),
            ],
            options={
                'verbose_name': 'Capítulo',
                'verbose_name_plural': 'Capítulos',
                'ordering': ['book', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Número')),
                ('text', models.TextField(verbose_name='Texto')),
                ('chapter', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='verses', to='bible_app.chapter', verbose_name='Capítulo')),
            ],
            options={
                'verbose_name': 'Versículo',
                'verbose_name_plural': 'Versículos',
                'ordering': ['chapter', 'number'],
            },
        ),
    ]
