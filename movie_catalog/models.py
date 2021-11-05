from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.db import models


class Movie(models.Model):
    category = models.ForeignKey(
        'Category',
        related_name='movies',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    tagline = models.CharField(max_length=255, blank=True, verbose_name='Слоган')
    poster = models.ImageField(upload_to='posters/', verbose_name='Постер')
    genre = models.ManyToManyField('Genre', related_name='movies', verbose_name='Жанр')
    country = models.ManyToManyField('Country', related_name='movies', verbose_name='Страна')
    director = models.ManyToManyField('Director', related_name='movies', verbose_name='Режиссер')
    actors = models.ManyToManyField('Actor', related_name='movies', verbose_name='Актеры')
    description = models.TextField(verbose_name='Описание')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    world_premiere = models.DateField(verbose_name='Премьера в мире')
    budget = models.PositiveIntegerField(default=0, verbose_name='Бюджет')
    fees = models.PositiveIntegerField(default=0, verbose_name='Сборы')
    age_limit = models.CharField(
        max_length=10,
        choices=[
            ('0', '0'),
            ('12', '12'),
            ('16', '16'),
            ('18', '18'),
        ],
        default='0',
        verbose_name='Возрастное ограничение',
    )
    available = models.BooleanField(default=True, verbose_name='Доступен')
    moderation = models.BooleanField(default=False, verbose_name='Модерация')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ('-world_premiere',)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Страну'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Имя')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    photo = models.ImageField(upload_to='directors/', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Режиссера'
        verbose_name_plural = 'Режиссеры'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Имя')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    photo = models.ImageField(upload_to='actors/', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Актера'
        verbose_name_plural = 'Актеры'

    def __str__(self):
        return self.name


class Comment(models.Model):
    movie = models.ForeignKey(
        Movie,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Фильм',
    )
    user = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    posted_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    text = models.TextField(max_length=5000, verbose_name='Текст')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Родитель',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.movie.title} - {self.text[:30]}'


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Фильм',
    )
    user = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    posted_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.movie.title} - {self.text[:30]}'


class RatingStar(models.Model):
    number = models.PositiveSmallIntegerField(default=0, verbose_name='Число')

    class Meta:
        verbose_name = 'Звезду рейтинга'
        verbose_name_plural = 'Звезды рейтинга'

    def __str__(self):
        return str(self.number)


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        related_name='ratings',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    movie = models.ForeignKey(
        Movie,
        related_name='ratings',
        on_delete=models.CASCADE,
        verbose_name='Фильм'
    )
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name='Звезда'
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def clean(self):
        if Rating.objects.filter(user=self.user, movie=self.movie):
            raise ValidationError('Пользователь уже поставил оценку этому фильму')

    def __str__(self):
        return f'{self.star} - {self.movie}'


class MovieShot(models.Model):
    movie = models.ForeignKey(
        Movie,
        related_name='movie_shots',
        on_delete=models.CASCADE,
        verbose_name='Фильм',
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(upload_to='movies_shots/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Кадр'
        verbose_name_plural = 'Кадры'

    def __str__(self):
        return self.title





