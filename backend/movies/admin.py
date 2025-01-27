from django.contrib import admin
from .models import Movie, MovieScrapeSession

admin.site.register(Movie)
admin.site.register(MovieScrapeSession)

