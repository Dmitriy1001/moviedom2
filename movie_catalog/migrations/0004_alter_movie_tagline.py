# Generated by Django 3.2.9 on 2021-11-02 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_catalog', '0003_alter_movie_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='tagline',
            field=models.CharField(blank=True, max_length=255, verbose_name='Слоган'),
        ),
    ]
