from datetime import datetime
from math import ceil

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
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
    comments_per_page = 10
    reviews_per_page = 5

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
        params = request.POST
        if 'star' in params:
            return self.post_review(request)
        elif 'del' in params:
            return self.delete_obj(request)
        else:
            return (
                self.post_comment(request) if not 'comment_id' in request.POST
                else self.update_comment(request)
            )

    def post_comment(self, request, **kwargs):
        movie = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            try:
                parent = Comment.objects.get(id=int(request.POST.get('parent')))
                comment_parent = parent if not parent.parent else parent.parent
            except TypeError:
                comment_parent = None
            if not comment_parent or (comment_parent and comment_parent.replies.count() < 10):
                new_comment.parent = comment_parent
                new_comment.movie = movie
                if not request.user.is_anonymous:
                    new_comment.user = request.user
                new_comment.save()
                msg = 'Комментарий добавлен' if not new_comment.parent else 'Ответ добавлен'
                extra_tags = new_comment.parent.id if new_comment.parent else new_comment.id
                page = 1 if not new_comment.parent else request.POST.get('page', 1)
            elif comment_parent and comment_parent.replies.count() == 10:
                msg = 'Максимальное кол-во ответов на комментарий - 10'
                extra_tags = comment_parent.id
                page = request.POST.get('page', 1)
            messages.info(request, msg, extra_tags=extra_tags)
            return redirect(
                '{}?tab=comments&com_p={}#com{}'.format(
                    reverse('movie_detail', args=(movie.category.slug, movie.slug)),
                    page,
                    extra_tags,
                )
            )

        self.object = self.get_object()
        context = self.get_context_data()
        context['comment_form'] = form
        context['anchor'] = '#formComment'
        return render(request, 'movie_catalog/movie_detail.html', context)

    def update_comment(self, request, **kwargs):
        print(request.POST, '!!!')
        movie = self.get_object()
        comment = Comment.objects.get(id=request.POST['comment_id'])
        comment_update_form = CommentForm(request.POST, instance=comment)
        page = request.POST.get('page', '1')
        if comment_update_form.is_valid():
            edited_comment = comment_update_form.save()
            extra_tags = request.POST.get('reply_parent', edited_comment.id)
            msg = (
                'Комментарий изменен' if not 'reply_number' in request.POST else
                f'Ответ №{request.POST["reply_number"]} изменен'
            )
            messages.info(request, msg, extra_tags=extra_tags)
            return redirect(
                '{}?tab=comments&com_p={}#com{}'.format(
                    reverse('movie_detail', args=(movie.category.slug, movie.slug)),
                    page,
                    extra_tags,
                )
            )
        self.object = self.get_object()
        context = self.get_context_data()
        context['none_parent_comments'] = (
            context['none_parent_comments'].paginator.get_page(int(page))
        )
        context['comment_update_form'] = comment_update_form
        context['edit'] = True
        context['edit_reply'] = True if 'reply_parent' in request.POST else False
        context['edited_comment'] = int(request.POST.get('reply_parent', comment.id))
        context['edited_reply'] = request.POST.get('comment_id')
        return render(request, 'movie_catalog/movie_detail.html', context)

    def delete_obj(self, request):
        movie = self.get_object()
        params = request.POST
        page = params['page']
        comment_id = int(params['com'])
        if 'com' in params:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            messages.info(request, 'Комментарий удален')
            return redirect(
                '{}?tab=comments&com_p={}'.format(
                    reverse('movie_detail', args=(movie.category.slug, movie.slug)),
                    page,
                )
            )


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
            messages.success(request, 'Рецензия добавлена', extra_tags=new_review.id)
            return redirect(
                '{}?tab=reviews&rev_p=1#tabs'.format(
                    reverse('movie_detail', args=(movie.category.slug, movie.slug))
                )
            )
        self.object = self.get_object()
        context = self.get_context_data()
        context['review_form'] = form
        context.update({'tab': 'reviews', 'anchor': '#formReview'})
        return render(request, 'movie_catalog/movie_detail.html', context)

    def pagination(self, queryset, per_page, page_name):
        for i in range(len(queryset)):
            queryset[i].index_number = len(queryset) - i
        paginator = Paginator(queryset, per_page)
        page_number = self.request.GET.get(page_name, 1)
        return paginator.get_page(page_number)

    def reviews_info(self, reviews):
        try:
            user_reviewed = reviews.filter(user=self.request.user).exists()
            if user_reviewed:
                user_review = reviews.get(user=self.request.user)
                user_review_index = list(reviews).index(user_review) + 1
                user_review_page_number = ceil(user_review_index / self.reviews_per_page)
            else:
                user_review_page_number = None
        except TypeError:
            user_reviewed = False
            user_review_page_number = None
        return {
            'user_reviewed': user_reviewed,
            'user_review_page_number': user_review_page_number,
            'reviews': self.pagination(reviews, self.reviews_per_page, 'rev_p')
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        context['title'] = movie.category.name
        context['tab'] = self.request.GET.get('tab')
        context['none_parent_comments'] = self.pagination(
            movie.comments.filter(parent=None).order_by('-posted_at'),
            self.comments_per_page,
            'com_p',
        )
        reviews = movie.reviews.all()
        if reviews:
            context.update(self.reviews_info(reviews))
        return context

class About(TemplateView):
    template_name = 'movie_catalog/about.html'
    extra_context = {'page': 'about'}