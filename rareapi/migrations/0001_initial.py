# Generated by Django 3.1.4 on 2020-12-22 02:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import rareapi.models.post


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='RareUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=500)),
                ('display_name', models.CharField(max_length=25, null=True)),
                ('profile_image_url', models.ImageField(blank=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image_url', models.ImageField(blank=True, upload_to=rareapi.models.post.Post.upload_to, verbose_name='Post Image')),
                ('content', models.CharField(max_length=2000)),
                ('approved', models.BooleanField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', related_query_name='post', to='rareapi.category')),
                ('rare_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', related_query_name='post', to='rareapi.rareuser')),
            ],
            options={
                'ordering': ['-publication_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('subject', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comment', to='rareapi.rareuser')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comment', to='rareapi.post')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
