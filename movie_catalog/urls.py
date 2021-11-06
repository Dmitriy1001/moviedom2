from django.urls import path

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('<slug:category>/', views.MovieList.as_view(), name='movie_list'),
]