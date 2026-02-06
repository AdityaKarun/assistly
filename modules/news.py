import logging
import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def get_news():
    """
    Fetches a small set of recent news headlines.

    Args:
        None

    Returns:
        str: Human-readable news summary, or error message on failure.
    """

    fallback = "Could not fetch news data"
    news_api_key = os.getenv("NEWS_API_KEY")

    if not news_api_key:
        logger.warning("NEWS_API_KEY not found in environment variables")
        return fallback

    try:
        logger.debug("Fetching top news headlines")

        # Initialize NewsAPI client and request headlines from a trusted source
        news_api = NewsApiClient(api_key=news_api_key)
        top_headlines = news_api.get_top_headlines(sources="bbc-news", language="en")
        articles = top_headlines.get("articles") or []

        headlines_list = []

        # Extract a limited number of headline titles for concise output
        for article in articles[:3]:
            headline_title = article.get("title")
            headlines_list.append(headline_title)

        if not headlines_list:
            logger.warning("Failed to fetch headlines")
            return fallback

        # Combine headlines into a readable sentence
        news_report = "Latest Headlines: " + ". ".join(headlines_list)

        logger.debug("News Report: %s", news_report)
        return news_report
    
    except Exception:
        logger.exception("Unexpected error while fetching news")
        return fallback
    
    
if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()
    get_news()
