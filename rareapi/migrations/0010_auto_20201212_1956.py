# Generated by Django 3.1.4 on 2020-12-12 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0009_auto_20201212_1954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-publication_date']},
        ),
    ]