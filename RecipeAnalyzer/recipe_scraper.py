import requests
from bs4 import BeautifulSoup
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class RecipeScraperInterface:
    """Interface for recipe scrapers."""
    def scrape(self, url: str) -> str:
        raise NotImplementedError

class DefaultRecipeScraper(RecipeScraperInterface):
    """Default implementation for scraping recipe text from a URL."""
    def scrape(self, url: str) -> str:
        # Validate URL
        validator = URLValidator()
        try:
            validator(url)
        except ValidationError:
            logger.error(f"Invalid URL: {url}")
            raise ValueError("Invalid URL")
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch URL: {url} | {e}")
            raise ValueError("Invalid or unreachable URL")
        try:
            soup = BeautifulSoup(resp.text, 'html.parser')
            all_text = '\n'.join([
                el.get_text(separator=' ', strip=True)
                for el in soup.find_all(['li', 'span', 'div', 'p'])
            ])
            return all_text
        except Exception as e:
            logger.error(f"Failed to parse recipe content: {e}")
            raise ValueError("Failed to parse recipe content")
