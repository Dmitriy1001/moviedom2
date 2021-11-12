from django import template
from django.db.models import Avg

from movie_catalog.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_similar_movies(current_movie:Movie):
    current_movie_genres = current_movie.genre.all()
    similar_movies = (
        Movie.objects.filter(
            available=True,
            moderation=True,
            category=current_movie.category,
            genre__in=current_movie_genres,
        )
        .exclude(slug=current_movie.slug)
        .distinct()
        .annotate(avg_rating=Avg('ratings__star__number'))
    )
    for movie in similar_movies:
        similar_genres = filter(lambda genre: genre in current_movie_genres, movie.genre.all())
        movie.similar_genres_count = len(list(similar_genres))
    return sorted(similar_movies, key=lambda movie: -movie.similar_genres_count)[:6]