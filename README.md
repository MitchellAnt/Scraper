# IMDb Web Scraper

A Django-based web application that scrapes and manages movie information from IMDb, featuring a REST API and a user-friendly web interface.

## 🎯 Features

- **Movie Data Scraping**
  - Scrapes detailed movie information from IMDb
  - Supports multiple genres
  - Handles pagination for comprehensive data collection
  - Random genre selection
  - Customizable number of pages to scrape

- **Data Points Collected**
  - Movie Title
  - Release Year
  - IMDb Rating
  - Director(s)
  - Cast Members
  - Plot Summary
  - Poster URL
  - Genre

- **Web Interface**
  - Interactive UI for scraping movies
  - Paginated movie display (10 movies per page)
  - Genre autocomplete suggestions
  - Random genre selection button
  - Visual indicators for newly added movies
  - Real-time scraping status updates

- **REST API Endpoints**
  - Movie listing with pagination
  - Genre-based filtering
  - Random genre selection
  - Scraping initiation
  - Movie statistics

## 🚀 Technologies Used

- Python 3.8+
- Django 4.x
- Django REST Framework
- Tailwind CSS
- JavaScript (Fetch API)
- SQLite/PostgreSQL

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/imdb-scraper.git
cd imdb-scraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

## 📋 Requirements

```text
django>=4.0.0
djangorestframework>=3.14.0
requests>=2.28.0
python-dotenv>=1.0.0
```

## 🎮 Usage

1. Access the web interface at `http://localhost:8000`

2. Enter a genre or use the "Random Genre" button

3. Specify the number of pages to scrape (1-10)

4. Click "Scrape Movies" to start the scraping process

5. View the results in the paginated display below

## 🔄 API Endpoints

- `GET /api/movies/`
  - List movies with pagination
  - Query parameters:
    - `genre`: Filter by genre
    - `page`: Page number
    - `refresh`: Boolean to refresh data

- `POST /api/movies/scrape/`
  - Initiate movie scraping
  - Body parameters:
    - `genre`: Movie genre to scrape
    - `max_pages`: Number of pages to scrape

- `GET /api/movies/random-genre/`
  - Get a random movie genre

## 🎯 Bonus Features Implemented

1. **Error Handling and Logging**
   - Comprehensive error handling in scraper
   - Detailed logging using Python's logging module
   - Separate logging configuration
   - User-friendly error messages in UI

2. **Performance Optimizations**
   - Efficient database queries using Django ORM
   - Pagination for better performance
   - Caching of scraped data
   - Optimized front-end rendering

3. **User Experience**
   - Real-time scraping status updates
   - Visual indicators for new movies
   - Genre suggestions
   - Random genre selection
   - Responsive design

4. **Data Management**
   - Automatic deduplication of movies
   - Scraping session tracking
   - Last updated timestamps
   - Genre-based organization

## 📝 Models

### Movie
```python
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True)
    imdb_rating = models.FloatField(default=0.0)
    directors = models.CharField(max_length=255, null=True)
    cast = models.JSONField(default=list)
    plot_summary = models.TextField(default="No plot available")
    poster_url = models.URLField(null=True)
    genre = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
```

### MovieScrapeSession
```python
class MovieScrapeSession(models.Model):
    genre = models.CharField(max_length=100)
    scraped_at = models.DateTimeField()
    total_movies = models.IntegerField(default=0)
    movies = models.ManyToManyField(Movie, related_name='scrape_sessions')
```

## 🔍 Scraping Process

1. The scraper uses IMDb's search functionality to find movies by genre
2. Extracts data from IMDb's Next.js data structure
3. Processes and cleans the extracted data
4. Stores unique movies in the database
5. Tracks scraping sessions for monitoring

## 🛠️ Error Handling

- Network request failures
- Invalid genre inputs
- Pagination errors
- Database connection issues
- Rate limiting detection
- Data parsing errors

## 📊 Logging

- Detailed logging of scraping process
- Error tracking
- Performance metrics
- Scraping session statistics


## 🧪 Testing

The project includes comprehensive test coverage for all major components:

### Test Categories

1. **Model Tests**
   - Movie model creation and validation
   - Field type verification
   - Relationship testing
   - Data integrity checks

2. **Scraper Tests**
   - Mock IMDb response handling
   - Data extraction verification
   - Pagination testing
   - Error handling verification

3. **API Tests**
   - Endpoint accessibility
   - Response format validation
   - Query parameter handling
   - Error response testing

4. **Integration Tests**
   - End-to-end scraping workflow
   - Database interaction
   - Session management
   - Response processing

### Running Tests

Run all tests:
```bash
python manage.py test
```

Run specific test categories:
```bash
python manage.py test movies.tests.MovieModelTests
python manage.py test movies.tests.MovieScraperTests
python manage.py test movies.tests.MovieAPITests
```

### Test Coverage

To generate a test coverage report:

1. Install coverage:
```bash
pip install coverage
```

2. Run tests with coverage:
```bash
coverage run manage.py test
```

3. Generate report:
```bash
coverage report
```

### Key Test Cases

1. **Model Testing**
   - Movie creation
   - Field validation
   - Relationship verification
   - Data type checking

2. **Scraper Testing**
   - Mock IMDb responses
   - Data extraction
   - Error handling
   - Session management

3. **API Testing**
   - GET /api/movies/
   - POST /api/movies/scrape/
   - GET /api/movies/random-genre/
   - Pagination handling
   - Filter validation

## 🧪 Future Improvements

1. Add unit tests for scraper and API endpoints
2. Implement asynchronous scraping
3. Add more advanced search filters
4. Implement user authentication
5. Add movie recommendations
6. Export functionality for scraped data

## ⚠️ Limitations

- Respect IMDb's robots.txt and terms of service
- Rate limiting considerations
- Dependent on IMDb's HTML structure
- Maximum of 10 pages per scraping session

<!-- ## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details. -->