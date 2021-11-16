from django.contrib import admin

from .models import Movie, Category, Genre, Country, Director, Actor, Comment, RatingStar, Review, MovieShot


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    ...


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    ...


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    ...


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    ...


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    ...


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'star', 'user')


@admin.register(MovieShot)
class MovieShotAdmin(admin.ModelAdmin):
    ...
