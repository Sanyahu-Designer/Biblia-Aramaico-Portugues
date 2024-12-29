from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0014_fix_wordcrossreference'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE dictionary_app_wordcrossreference DROP COLUMN IF EXISTS created_at;",
            "SELECT 1;"  # No-op reverse SQL
        ),
    ]
