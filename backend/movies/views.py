from django.shortcuts import render
from django.db.models import Q, Count, Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Movie
from .imdb_scraper import scrape_movies_by_genre
from django.utils import timezone

class MoviePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

def movie_scraper_view(request):
    return render(request, 'movies/scraper.html')

@api_view(['POST'])
def scrape_movies(request):
    genre = request.data.get('genre', 'comedy')
    max_pages = request.data.get('max_pages', 3)

    try:
        # First, get existing movies count for this genre
        existing_movies = Movie.objects.filter(genre__iexact=genre).count()
        
        # Scrape new movies
        new_movies = scrape_movies_by_genre(genre, max_pages)
        
        return Response({
            'status': 'success',
            'existing_movies': existing_movies,
            'new_movies_scraped': len(new_movies),
            'total_movies': existing_movies + len(new_movies)
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['GET'])
def movie_list_view(request):
    genre = request.GET.get('genre', 'comedy')
    refresh = request.GET.get('refresh', 'false').lower() == 'true'
    
    # Create a queryset for the specified genre
    movies_queryset = Movie.objects.filter(genre__iexact=genre)
    
    # Check if we need to refresh data
    if refresh or not movies_queryset.exists():
        try:
            # Scrape one page of new movies
            new_movies = scrape_movies_by_genre(genre, max_pages=1)
            movies_queryset.update(last_updated=timezone.now())
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f"Error refreshing movies: {str(e)}"
            }, status=400)
    
    # Get all movies for the genre, ordered by multiple criteria
    movies = movies_queryset.select_related().order_by(
        '-release_year',
        '-imdb_rating'
    )
    
    # Initialize paginator
    paginator = MoviePagination()
    paginated_movies = paginator.paginate_queryset(movies, request)
    
    # Prepare movie data
    movie_data = [{
        'title': movie.title,
        'release_year': movie.release_year,
        'imdb_rating': movie.imdb_rating,
        'directors': movie.directors,
        'last_updated': movie.last_updated,
        'is_new': movie.last_updated and (timezone.now() - movie.last_updated).days < 1
    } for movie in paginated_movies]
    
    return Response({
        'status': 'success',
        'count': movies.count(),
        'results': movie_data,
        'current_page': request.GET.get('page', 1),
        'total_pages': (movies.count() + paginator.page_size - 1) // paginator.page_size
    })