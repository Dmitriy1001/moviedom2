# Generated by Django 3.2.9 on 2021-11-11 16:11

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movie_catalog', '0013_ratingstar_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='video',
            field=embed_video.fields.EmbedVideoField(null=True),
        ),
    ]