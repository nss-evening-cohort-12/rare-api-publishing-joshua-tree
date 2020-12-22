# Generated by Django 3.1.4 on 2020-12-19 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='rare_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', related_query_name='post', to='rareapi.rareuser'),
        ),
    ]
