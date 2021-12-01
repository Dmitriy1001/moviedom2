from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView

from movie_catalog.forms import CommentForm, ReviewForm
from movie_catalog.models import Movie, Category, Actor, Director, Country, Genre, Comment, Review, RatingStar


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
            .annotate(avg_rating=Avg('reviews__star__number'))
            .order_by('-avg_rating')
        )[:10]
        # new movies
        context['new_all'] = (
            Movie.objects.filter(available=True, moderation=True)
            .annotate(avg_rating=Avg('reviews__star__number'))
        )[:6]
        context['new_films'] = (
            Movie.objects.filter(available=True, moderation=True, category__slug='films')
            .annotate(avg_rating=Avg('reviews__star__number'))
        )[:6]
        context['new_cartoons'] = (
            Movie.objects.filter(available=True, moderation=True, category__slug='cartoons')
            .annotate(avg_rating=Avg('reviews__star__number'))
        )[:6]
        context['new_series'] = (
            Movie.objects.filter(available=True, moderation=True, category__slug='series')
            .annotate(avg_rating=Avg('reviews__star__number'))
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
            .annotate(avg_rating=Avg('reviews__star__number'))
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
                Movie.objects.annotate(avg_rating=Avg('reviews__star__number'))
                .filter(avg_rating__range=(star, star + 0.9))
            )
            self.kwargs['title'] = star
            flags['by_rating'] = True
        # by year
        elif self.kwargs['model'] == 'year':
            movies = (
                Movie.objects.annotate(avg_rating=Avg('reviews__star__number'))
                .filter(year=self.kwargs['instance'])
            )
            self.kwargs['title'] = self.kwargs['instance']
            flags['by_year'] = True
        # by related model(Genre, Country, Director, Actor)
        else:
            model = self.models[self.kwargs['model']]
            model_instance = model.objects.get(slug=self.kwargs['instance'])
            movies = model_instance.movies.annotate(avg_rating=Avg('reviews__star__number'))
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
            .annotate(avg_rating=Avg('reviews__star__number'))
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET.get('search')
        return context


class MovieDetail(DetailView):
    extra_context = {'page': 'movie_detail'}

    def get_queryset(self):
        return (
            Movie.objects.filter(
                category__slug=self.kwargs['category'],
                available=True,
                moderation=True,
            )
            .annotate(avg_rating=Avg('reviews__star__number'))
        )

    def get_object(self):
        return self.get_queryset().get(slug=self.kwargs['movie_slug'])

    def post(self, request, **kwargs):
        if 'star' in request.POST:
            return self.post_review(request)
        else:
            return self.post_comment(request)

    def post_comment(self, request, **kwargs):
        movie = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            if request.POST.get('parent', None):
                parent = Comment.objects.get(id=int(request.POST.get('parent')))
                new_comment.parent = parent if not parent.parent else parent.parent
            new_comment.movie = movie
            if not request.user.is_anonymous:
                new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect('movie_detail', movie.category.slug, movie.slug)
        self.object = self.get_object()
        context = self.get_context_data()
        context['comment_form'] = form
        return render(request, 'movie_catalog/movie_detail.html', context)

    @method_decorator(login_required)
    def post_review(self, request, **kwargs):
        movie = self.get_object()
        review_form_data = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'title': request.POST['title'],
            'text': request.POST['text'],
            'star': RatingStar.objects.get(number=float(request.POST['star'])),
        }
        form = ReviewForm(review_form_data)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.movie = movie
            new_review.user = request.user
            try:
                new_review.clean()
            except ValidationError:
                return redirect('movie_detail', movie.category.slug, movie.slug)
            new_review.save()
            messages.success(request, 'Рецензия добавлена')
            return redirect('movie_detail', movie.category.slug, movie.slug)
        self.object = self.get_object()
        context = self.get_context_data()
        context['review_form'] = form
        return render(request, 'movie_catalog/movie_detail.html', context)

    def pagination(self, queryset, per_page, page_name):
        paginator = Paginator(queryset, per_page)
        page_number = self.request.GET.get(page_name, 1)
        return paginator.get_page(page_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        reviews = movie.reviews.all()
        context['title'] = movie.category.name
        context['none_parent_comments'] = (
            self.pagination(movie.comments.filter(parent=None), 3, 'com_p')
        )
        context['reviews'] = self.pagination(reviews, 1, 'rev_p')
        try:
            context['user_reviewed'] = reviews.filter(user=self.request.user).exists()
        except TypeError:
            context['user_reviewed'] = False
        context['tab'] = self.request.GET.get('tab')
        return context

class About(TemplateView):
    template_name = 'movie_catalog/about.html'
    extra_context = {'page': 'about'}