from datetime import datetime

from django.db.models import Avg, Min, Max
from django.http import Http404
from django.views.generic import TemplateView, ListView

from movie_catalog.models import Movie, Category, Actor, Director, Country, Genre


class Index(TemplateView):
    template_name = 'movie_catalog/index.html'
    extra_context = {'page': 'index'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # top movies
        current_date = datetime.today()
        current_date_minus_year = datetime(
            current_date.year - 1,
            current_date.month,
            current_date.day - (1 if current_date.month == 2 and current_date.day == 29 else 0),
        )
        context['top_movies_for_year'] = (
            Movie.objects.filter(
                world_premiere__range=(current_date_minus_year, current_date),
                available=True,
                moderation=True,
            )
            .annotate(avg_rating=Avg('ratings__star__number'))
            .order_by('-avg_rating')
        )[:10]
        # new movies
        context['new_all'] = (
            Movie.objects.filter(available=True, moderation=True)
            .annotate(avg_rating=Avg('ratings__star__number'))
        )[:6]
        context['new_films'] = (
            Movie.objects.filter(available=True, moderation=True, category__slug='films')
            .annotate(avg_rating=Avg('ratings__star__number'))
        )[:6]
        context['new_cartoons'] = (
            Movie.objects.filter(available=True, moderation=True, category__slug='cartoons')
            .annotate(avg_rating=Avg('ratings__star__number'))
        )[:6]
        context['new_series'] = (
            Movie.objects.filter(available=True, moderation=True, category__slug='series')
            .annotate(avg_rating=Avg('ratings__star__number'))
        )[:6]
        # expected movies
        context['expected_movies'] = Movie.objects.filter(available=False, moderation=True)
        return context


class MovieList(ListView):
    model = Movie
    paginate_by = 8
    extra_context = {'page': 'movie_list'}

    def get_queryset(self):
        movies = (
            Movie.objects.filter(available=True, moderation=True)
            .annotate(avg_rating=Avg('ratings__star__number'))
        )
        if self.kwargs['category'] == 'all':
            self.kwargs['title'] = None
            return movies
        try:
            category = Category.objects.get(slug=self.kwargs['category'])
            self.kwargs['title'] = category.name
            return movies.filter(category=category)
        except Category.DoesNotExist:
            raise Http404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs.get('title')
        return context


class Filter(MovieList):
    models = {'genre': Genre, 'country': Country, 'director': Director, 'actor': Actor}
    paginate_by = 12
    extra_context = {'page': 'movie_grid'}

    def get_queryset(self):
        print(type(self.kwargs['instance']), '!!!')
        if self.kwargs['model'] != 'rating':
            model = self.models[self.kwargs['model']]
            model_instance = model.objects.get(slug=self.kwargs['instance'])
            movies = model_instance.movies.annotate(avg_rating=Avg('ratings__star__number'))
            self.kwargs['title'] = model_instance.name
        else:
            star = int(float(self.kwargs['instance']))
            movies = (
                Movie.objects.annotate(avg_rating=Avg('ratings__star__number'))
                .filter(avg_rating__range=(star, star+0.9))
            )
            self.kwargs['title'] = star
        return movies.filter(available=True, moderation=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['title']
        return context


class About(TemplateView):
    template_name = 'movie_catalog/about.html'
    extra_context = {'page': 'about'}