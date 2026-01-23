import os
import requests
from dotenv import load_dotenv

from modules.location import get_location

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

    weather_api_key  = os.getenv("WEATHER_API_KEY")

    if not weather_api_key:
        print("WEATHER_API_KEY not found in environment variables.")

    if "location" in payload:
        city = payload.get("location")
        print(payload)
    else:
        city = get_location()

    # Abort if location cannot be resolved
    if not city:
        return "Could not determine your location for weather report."

    try:
    
        response = requests.get(
            "https://api.weatherapi.com/v1/current.json",
            params={"key": weather_api_key, "q": city},
            timeout=10
            )
        weather_data = response.json()

        condition = weather_data["current"]["condition"]["text"]
        temperature = weather_data["current"]["temp_c"]
        wind_speed = weather_data["current"]["wind_kph"]

        weather_report = (
            f"Currently in {city}, it's {condition} with a temperature of "
            f"{temperature} degrees Celsius and wind speed of {wind_speed} kilometers per hour."
        )

        return weather_report
    
    except Exception:
        return f"Could not fetch weather data."


if __name__ == "__main__":
    print("Weather Report...")
    city = input("Enter city: ")

    if not city:
        payload = {}
    else:
        payload = {"location": city}

    weather_report = get_weather(payload)
    print(weather_report)
