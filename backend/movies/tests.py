from django.test import TestCase
from django.utils import timezone
from movies.models import Movie, MovieScrapeSession
from movies.imdb_scraper import IMDbScraper
import responses
import json

class IMDbScraperTests(TestCase):
    @responses.activate
    def test_movie_scraping(self):
        """
        Test movie scraping functionality
        """
        # Mock IMDb search and movie page responses
        responses.add(
            responses.GET, 
            IMDbScraper.BASE_URL + "/search/title/",
            body=self._mock_search_page(),
            status=200
        )
        
        # Run scraper
        movies = IMDbScraper.scrape_movies('comedy', max_pages=1)
        
        # Assertions
        self.assertTrue(len(movies) > 0)
        self.assertEqual(MovieScrapeSession.objects.count(), 1)
        self.assertTrue(Movie.objects.exists())

    def _mock_search_page(self):
        """
        Generate mock search page HTML
        """
        # Implement mock HTML generation logic
        return "<html>Mock Search Results</html>"