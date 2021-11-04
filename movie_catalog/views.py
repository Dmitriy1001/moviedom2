from datetime import datetime

from django.db.models import Avg
from django.views.generic import TemplateView, ListView

from movie_catalog.models import Movie


class Index(TemplateView):
    template_name = 'movie_catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.today()
        current_date_minus_year = datetime(
            current_date.year - 1,
            current_date.month,
            current_date.day - (1 if current_date.month == 2 and current_date.day == 29 else 0),
        )
        context['top_movies_for_year'] = (
            Movie.objects.filter(world_premiere__range=(current_date_minus_year, current_date))
            .annotate(avg_rating=Avg('ratings__star__number'))
            .order_by('-avg_rating')
        )[:10]
        context['new_films'] = Movie.objects.filter(category__slug='films')
        context['new_cartoons'] = Movie.objects.filter(category__slug='cartoons')
        context['new_series'] = Movie.objects.filter(category__slug='series')
        return context