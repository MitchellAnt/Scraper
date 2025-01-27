import traceback
import requests
import json
from django.utils import timezone
from .models import Movie, MovieScrapeSession
from .logging_config import logger

BASE_URL = "https://www.imdb.com"

def scrape_movies_by_genre(genre, max_pages=5):
    """
    Scrape movies by genre from IMDb

    :param genre: Movie genre to scrape
    :param max_pages: Maximum number of pages to scrape
    :return: List of scraped movies
    """
    start = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    movies = []
    page_count = 0

    # Create scrape session
    scrape_session = MovieScrapeSession.objects.create(
        genre=genre,
        scraped_at=timezone.now()
    )
    max_pages = int(max_pages)
    try:
        while int(page_count) < int(max_pages):
            search_url = f"{BASE_URL}/search/title/?genres={genre}&start={start}&explore=title_type,genres"
            logger.info(f"Processing page: {search_url}")

            response = requests.get(search_url, headers=headers)
            if response.status_code != 200:
                logger.warning(f"Failed to retrieve page: {response.status_code}")
                break

            # Extract __NEXT_DATA__ JSON
            start_tag = '<script id="__NEXT_DATA__" type="application/json">'
            end_tag = '</script>'
            start_index = response.text.find(start_tag) + len(start_tag)
            end_index = response.text.find(end_tag, start_index)
            json_data = response.text[start_index:end_index]
            data = json.loads(json_data)

            # Extract movie details from JSON
            for movie in data['props']['pageProps']['searchResults']['titleResults']['titleListItems']:
                title = movie.get('titleText', '')
                release_year = movie.get('releaseYear', None)
                imdb_rating = movie.get('ratingSummary', {}).get('aggregateRating', None)
                plot = movie.get('plot', '')
                poster_url = movie.get('primaryImage', {}).get('url', None)
                directors = movie.get('directors', '')
                cast = movie.get('topCast', '')

                # Clean and process fields
                director = directors.split('|')[0].strip() if directors else None
                cast_list = cast.split('|') if '|' in cast else [cast]

                # Create or get movie object
                movie_obj, created = Movie.objects.get_or_create(
                    title=title,
                    defaults={
                        'release_year': release_year,
                        'imdb_rating': imdb_rating if imdb_rating else 0.0,
                        'directors': director,
                        'cast': cast_list,
                        'plot_summary': plot or "No plot available",
                        'poster_url': poster_url,
                        'genre':genre
                    }
                )

                # Associate with scrape session
                movie_obj.scrape_sessions.add(scrape_session)

                movies.append({
                    "title": title,
                    "release_year": release_year,
                    "imdb_rating": imdb_rating,
                    "plot": plot,
                    "poster_url": poster_url,
                    "cast": cast_list
                })

            # Increment the `start` parameter for pagination
            start += 50
            page_count += 1

        # Update scrape session
        scrape_session.total_movies = len(movies)
        scrape_session.save()

        return movies

    except Exception as e:
        logger.error(f"Scraping failed for genre {genre}: {e}")
        logger.error(traceback.format_exc())
        scrape_session.delete()
        raise
