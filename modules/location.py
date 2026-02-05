import logging
import requests

logger = logging.getLogger(__name__)

def get_location():
    """
    Determines the current city based on public IP address.

    Args:
        None

    Returns:
        str: City name if available, otherwise an error message.
    """
    url = "https://ipinfo.io/json"
    timeout=10
    fallback = "Could not fetch location data"

    try:
        response = requests.get(url, timeout=timeout)
        logger.debug(
            "API request to IPinfo | URL=%s Timeout=%s",
            url,
            timeout
        )
        
        logger.debug(
            "API response from IPinfo | Status=%s",
            response.status_code,
        )
        
        # Raises exception for non-2xx responses
        response.raise_for_status()

        # Decode JSON response from IPinfo into Python objects
        data = response.json()
        logger.debug("Parsed JSON response from IPinfo: %s", data)

        city = data.get("city", fallback)
        logger.debug("Detected location: %s", city)

        return city
    
    except requests.RequestException as e:
        # Network issues, timeouts, or non-2xx HTTP responses
        logger.warning("HTTP/network error calling IPinfo API: %s", e)
        return fallback
    
    except Exception:
        # Unexpected programming or runtime error
        logger.exception("Unexpected error while fetching location")
        return fallback


if __name__ == "__main__":
    from core.logger_config import setup_logging
    
    setup_logging()
    get_location()
