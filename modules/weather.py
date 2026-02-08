import logging
import os
import requests
from dotenv import load_dotenv

from modules.location import get_location

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def get_weather(payload):
    """
    Retrieves current weather information for a given city or inferred location.

    Args:
        payload (dict): Intent entities that may contain a location value.

    Returns:
        str: Human-readable weather report or error message.
    """

    logger.debug("Payload received: %s", payload)

    url = "https://api.weatherapi.com/v1/current.json"
    fallback = "Could not fetch weather data"
    timeout=10
    weather_api_key = os.getenv("WEATHER_API_KEY")

    if not weather_api_key:
        logger.warning("WEATHER_API_KEY not found in environment variables")
        return fallback

    if "location" in payload:
        city = payload.get("location")
        logger.debug("Using location from payload")
    else:
        logger.debug("No location in payload, resolving via IP")
        city = get_location()

    # Abort if location cannot be resolved
    if not city:
        logger.warning("Unable to resolve location for weather request")
        return fallback

    try:
        response = requests.get(url, params={"key": weather_api_key, "q": city}, timeout=timeout)

        logger.debug(
            "API request to WeatherAPI | URL=%s Timeout=%s",
            url,
            timeout
        )
        
        logger.debug(
            "API response from WeatherAPI | Status=%s",
            response.status_code,
        )

        # Raises exception for non-2xx responses
        response.raise_for_status()

        # Decode JSON response from WeatherAPI into Python objects
        weather_data = response.json()
        logger.debug("Parsed JSON response from WeatherAPI: %s", weather_data)

        condition = weather_data["current"]["condition"]["text"]
        temperature = weather_data["current"]["temp_c"]
        wind_speed = weather_data["current"]["wind_kph"]

        weather_report = (
            f"Currently in {city}, it's {condition} with a temperature of "
            f"{temperature} degrees Celsius and wind speed of {wind_speed} kilometers per hour"
        )

        logger.debug("Weather Report: %s", weather_report)
        return weather_report
    
    except requests.RequestException as e:
        # Network issues, timeouts, or non-2xx HTTP responses
        logger.warning("HTTP/network error calling Weather API: %s", e)
        return fallback
    
    except Exception:
        # Unexpected programming or runtime error
        logger.exception("Unexpected error while fetching weather")
        return fallback


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()

    city = input("Enter city: ")

    if not city:
        payload = {}
    else:
        payload = {"location": city}

    get_weather(payload)
