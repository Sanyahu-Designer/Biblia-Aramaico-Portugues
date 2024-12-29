from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0013_merge_20241224_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordcrossreference',
            name='reference_word',
        ),
        migrations.AddField(
            model_name='wordcrossreference',
            name='reference',
            field=models.ForeignKey('bible_app.Verse', verbose_name='Referência', on_delete=models.CASCADE, null=True),
        ),
    ]
