# Generated by Django 3.2.9 on 2021-11-10 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_catalog', '0012_alter_movie_age_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingstar',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]