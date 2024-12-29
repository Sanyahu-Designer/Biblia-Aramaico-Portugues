from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0011_alter_aramaicword_aramaic_word_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FavoriteWord',
        ),
    ]
