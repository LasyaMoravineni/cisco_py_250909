"""
scraper.py - Web scraping utility for HMS
Fetches patient-related articles/news from an external website.
"""

import requests
from bs4 import BeautifulSoup
from hms.app.exceptions import HMSException
from hms.app.logger import logger


class ScraperError(HMSException):  # pylint: disable=too-few-public-methods
    """Raised when scraping fails"""
    pass


def scrape_medical_news(url="https://example.com/medical-news", limit=5):
    """
    Scrape medical news headlines and links from the given URL.

    Args:
        url (str): Website URL to scrape
        limit (int): Maximum number of articles to return

    Returns:
        list[dict]: List of {title, link} dictionaries
    """
    try:
        logger.info("Scraping medical news from %s", url)
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            logger.error("Failed to fetch page, status: %s", response.status_code)
            raise ScraperError(f"Website returned status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Dummy structure: adjust selectors based on real site
        articles = soup.find_all("a", class_="news-link", limit=limit)

        results = []
        for article in articles:
            title = article.get_text(strip=True)
            link = article.get("href")
            results.append({"title": title, "link": link})

        logger.info("Successfully scraped %d articles", len(results))
        return results

    except requests.RequestException as e:
        logger.exception("Network error during scraping")
        raise ScraperError(f"Network error: {str(e)}") from e
    except Exception as e:
        logger.exception("Unexpected error during scraping")
        raise ScraperError(str(e)) from e


if __name__ == "__main__":
    # Run standalone for quick test
    news = scrape_medical_news()
    for idx, item in enumerate(news, start=1):
        print(f"{idx}. {item['title']} ({item['link']})")
