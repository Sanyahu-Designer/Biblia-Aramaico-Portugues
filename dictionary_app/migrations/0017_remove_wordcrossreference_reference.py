from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0016_add_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordcrossreference',
            name='reference',
        ),
    ]
