import requests

def get_location():
    """
    Determines the current city based on public IP address.

    Args:
        None

    Returns:
        str: City name if available, otherwise an error message.
    """
    try:
        response = requests.get("https://ipinfo.io/json", timeout=10)
        data = response.json()

        city = data.get("city")

        return city
    
    except Exception as e:
        return f"Could not fetch location data."


if __name__ == "__main__":

    city = get_location()
    if city:
        print(f"You are currently in: {city}")
    else:
        print("Unable to fetch location info.")
