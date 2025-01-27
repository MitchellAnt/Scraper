from django.db import models
from django.utils import timezone

class MovieScrapeSession(models.Model):
    """Track individual scrape sessions to prevent duplicate entries"""
    genre = models.CharField(max_length=100)
    scraped_at = models.DateTimeField(default=timezone.now)
    total_movies = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.genre} - {self.scraped_at}"

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True, blank=True)
    imdb_rating = models.FloatField(null=True, blank=True)
    directors = models.JSONField(default=list, null=True, blank=True)
    cast = models.JSONField(default=list)
    plot_summary = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    scrape_sessions = models.ManyToManyField(MovieScrapeSession, related_name='movies')
    poster_url = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('title', 'release_year')

    def __str__(self):
        return f"{self.title} ({self.release_year})"