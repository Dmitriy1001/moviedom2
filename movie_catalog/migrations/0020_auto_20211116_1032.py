# Generated by Django 3.2.9 on 2021-11-16 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_catalog', '0019_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='posted_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Опубликовано'),
        ),
        migrations.AddField(
            model_name='rating',
            name='text',
            field=models.TextField(blank=True, verbose_name='Текст'),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]