from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_scraper_view, name='scraper'),
    path('api/movies/scrape/', views.scrape_movies, name='scrape_movies'),
    path('api/movies/', views.movie_list_view, name='movie_list'),
    path('api/movies/random-genre/', views.random_genre, name='random_genre'),
]