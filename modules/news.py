import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_news():
    """
    Fetches a small set of recent news headlines.

    Args:
        None

    Returns:
        list | str: List of headline strings, or error message on failure.
    """
    news_api_key = os.getenv("NEWS_API_KEY")

    if not news_api_key:
        print("NEWS_API_KEY not found in environment variables.")

    try:
        new_api = NewsApiClient(api_key=news_api_key)
        top_headlines = new_api.get_top_headlines(sources="bbc-news", language="en")
        articles = top_headlines["articles"]

        headlines_list = []

        for article in articles[:3]:
            headline_title = article.get("title")
            headlines_list.append(headline_title)

        return headlines_list
    
    except Exception:
        return f"Could not fetch news."
    
    
if __name__ == "__main__":
    print("Here are the top news headlines.")
    news_report = get_news()
    print(news_report)
