from datetime import datetime

from django.db.models import Avg
from django.http import Http404
from django.views.generic import TemplateView, ListView

from movie_catalog.models import Movie, Category


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
        context['title'] = self.kwargs['title']
        return context


class About(TemplateView):
    template_name = 'movie_catalog/about.html'
    extra_context = {'page': 'about'}