# Generated by Django 3.1.4 on 2021-01-12 02:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rareuser',
            options={'ordering': ['display_name']},
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('ended_on', models.DateTimeField(blank=True)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_subscriptions', related_query_name='author_subscription', to='rareapi.rareuser')),
                ('follower_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_subscriptions', related_query_name='follower_subscription', to='rareapi.rareuser')),
            ],
        ),
    ]
