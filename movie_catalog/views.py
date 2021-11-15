from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView

from movie_catalog.forms import CommentForm
from movie_catalog.models import Movie, Category, Actor, Director, Country, Genre, Comment


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
        flags = {'by_rating': False, 'by_year': False}
        # by rating
        if self.kwargs['model'] == 'rating':
            star = int(float(self.kwargs['instance']))
            movies = (
                Movie.objects.annotate(avg_rating=Avg('ratings__star__number'))
                .filter(avg_rating__range=(star, star + 0.9))
            )
            self.kwargs['title'] = star
            flags['by_rating'] = True
        # by year
        elif self.kwargs['model'] == 'year':
            print(type(self.kwargs['instance']), '!!!')
            movies = (
                Movie.objects.annotate(avg_rating=Avg('ratings__star__number'))
                .filter(year=self.kwargs['instance'])
            )
            self.kwargs['title'] = self.kwargs['instance']
            flags['by_year'] = True
        # by related model(Genre, Country, Director, Actor)
        else:
            model = self.models[self.kwargs['model']]
            model_instance = model.objects.get(slug=self.kwargs['instance'])
            movies = model_instance.movies.annotate(avg_rating=Avg('ratings__star__number'))
            self.kwargs['title'] = model_instance.name

        self.kwargs['flags'] = flags
        return movies.filter(available=True, moderation=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['title']
        context.update(self.kwargs['flags'])
        return context


class Search(MovieList):
    paginate_by = 12
    extra_context = {'page': 'movie_grid', 'search': True}

    def get_queryset(self):
        try:
            query = self.request.GET['search'].strip()
        except KeyError:
            query = ''
        return (
            Movie.objects.filter(available=True, moderation=True)
            .filter(Q(title__icontains=query) | Q(description__icontains=query))
            .annotate(avg_rating=Avg('ratings__star__number'))
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET.get('search')
        return context


class MovieDetail(DetailView):
    extra_context = {'page': 'movie_detail'}
    form_class = CommentForm

    def get_queryset(self):
        return (
            Movie.objects.filter(
                category__slug=self.kwargs['category'],
                available=True,
                moderation=True,
            )
            .annotate(avg_rating=Avg('ratings__star__number'))
        )

    def get_object(self):
        return self.get_queryset().get(slug=self.kwargs['movie_slug'])

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        movie = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            if request.POST.get('parent', None):
                parent = Comment.objects.get(id=int(request.POST.get('parent')))
                new_comment.parent = parent if not parent.parent else parent.parent
            new_comment.movie = movie
            new_comment.user = request.user
            new_comment.save()
            return redirect('movie_detail', movie.category.slug, movie.slug)
        return render(request, self.template_name, {'movie': movie, 'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        context['title'] = movie.category.name
        context['none_parent_comments'] = movie.comments.filter(parent=None)
        return context

class About(TemplateView):
    template_name = 'movie_catalog/about.html'
    extra_context = {'page': 'about'}