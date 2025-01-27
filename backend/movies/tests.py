from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from movies.models import Movie, MovieScrapeSession
from movies.imdb_scraper import scrape_movies_by_genre
import responses
import json

class MovieModelTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            release_year=2024,
            imdb_rating=8.5,
            directors="Test Director",
            cast=["Actor 1", "Actor 2"],
            plot_summary="Test plot",
            genre="comedy"
        )

    def test_movie_creation(self):
        """Test movie model creation and fields"""
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.release_year, 2024)
        self.assertEqual(self.movie.imdb_rating, 8.5)
        self.assertEqual(self.movie.genre, "comedy")
        self.assertIsInstance(self.movie.cast, list)

class MovieScraperTests(TestCase):
    @responses.activate
    def test_movie_scraping(self):
        """Test movie scraping functionality"""
        # Mock IMDb response with actual JSON structure
        mock_data = {
            "props": {
                "pageProps": {
                    "searchResults": {
                        "titleResults": {
                            "titleListItems": [
                                {
                                    "titleText": "Test Movie",
                                    "releaseYear": 2024,
                                    "ratingSummary": {"aggregateRating": 8.5},
                                    "plot": "Test plot",
                                    "directors": "Test Director",
                                    "topCast": "Actor 1|Actor 2"
                                }
                            ]
                        }
                    }
                }
            }
        }

        # Create mock HTML with embedded JSON
        mock_html = f'''
        <html>
            <script id="__NEXT_DATA__" type="application/json">
            {json.dumps(mock_data)}
            </script>
        </html>
        '''

        # Mock the IMDb endpoint
        responses.add(
            responses.GET,
            "https://www.imdb.com/search/title/",
            body=mock_html,
            status=200
        )

        # Run scraper
        movies = scrape_movies_by_genre('comedy', max_pages=1)

        # Verify results
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]['title'], "Test Movie")
        self.assertEqual(movies[0]['release_year'], 2024)
        self.assertEqual(movies[0]['imdb_rating'], 8.5)

class MovieAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            title="Test Movie",
            release_year=2024,
            imdb_rating=8.5,
            directors="Test Director",
            cast=["Actor 1", "Actor 2"],
            plot_summary="Test plot",
            genre="comedy"
        )

    def test_movie_list_api(self):
        """Test movie list API endpoint"""
        response = self.client.get(reverse('movie-list'), {'genre': 'comedy'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.json()['results']) > 0)

    def test_random_genre_api(self):
        """Test random genre API endpoint"""
        response = self.client.get(reverse('random-genre'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('genre', response.json())

    def test_scrape_movies_api(self):
        """Test movie scraping API endpoint"""
        data = {
            'genre': 'comedy',
            'max_pages': 1
        }
        response = self.client.post(
            reverse('scrape-movies'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'success')

class MovieScrapeSessionTests(TestCase):
    def test_scrape_session_creation(self):
        """Test scrape session creation and relationship with movies"""
        # Create a movie
        movie = Movie.objects.create(
            title="Test Movie",
            release_year=2024,
            genre="comedy"
        )

        # Create a scrape session
        session = MovieScrapeSession.objects.create(
            genre="comedy",
            scraped_at=timezone.now()
        )
        session.movies.add(movie)

        # Verify relationship
        self.assertEqual(session.movies.count(), 1)
        self.assertEqual(movie.scrape_sessions.count(), 1)