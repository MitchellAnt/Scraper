import logging
import traceback
from django.conf import settings
import os

# Configure logging
LOG_DIR = os.path.join(settings.BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'imdb_scraper.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)