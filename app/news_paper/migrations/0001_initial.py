# Generated by Django 4.2.2 on 2023-06-15 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(default=0)),
                ('authorUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=65, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newsOrArt', models.CharField(choices=[('NW', 'Новость'), ('AC', 'Статья')], default='NW', max_length=2)),
                ('dateCreate', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=128)),
                ('text', models.TextField()),
                ('rating', models.SmallIntegerField(default=0)),
                ('postAuthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_paper.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catTR', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_paper.category')),
                ('postTR', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_paper.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='postCategory',
            field=models.ManyToManyField(through='news_paper.PostCategory', to='news_paper.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('dateCreate', models.DateTimeField(auto_now_add=True)),
                ('rating', models.SmallIntegerField(default=0)),
                ('commentPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_paper.post')),
                ('commentUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
