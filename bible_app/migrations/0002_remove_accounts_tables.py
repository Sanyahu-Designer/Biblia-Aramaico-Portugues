from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('bible_app', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            # SQL para remover as tabelas
            """
            DROP TABLE IF EXISTS accounts_userprofile;
            """,
            # SQL para reverter (não implementado pois estamos removendo o app)
            """
            """
        ),
    ]
