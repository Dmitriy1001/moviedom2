# Generated by Django 3.2.9 on 2021-11-04 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_catalog', '0007_alter_movie_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Доступен'),
        ),
    ]
