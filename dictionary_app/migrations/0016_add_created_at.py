from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0015_remove_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordcrossreference',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data de Criação'),
            preserve_default=False,
        ),
    ]
