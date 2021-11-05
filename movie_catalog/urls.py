from django.urls import path

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<slug:category>/', views.MovieList.as_view(), name='movie_list'),
]