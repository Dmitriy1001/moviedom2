# Generated by Django 3.2.9 on 2021-11-15 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_catalog', '0015_auto_20211111_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movie_catalog.comment', verbose_name='Родитель'),
        ),
    ]
