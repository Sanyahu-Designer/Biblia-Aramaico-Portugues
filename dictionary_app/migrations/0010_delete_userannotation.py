# Generated by Django 5.1.2 on 2024-12-24 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0009_alter_aramaicword_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAnnotation',
        ),
    ]
