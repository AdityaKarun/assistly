import logging
import pywhatkit

logger = logging.getLogger(__name__)

def youtube_player(payload):
    """
    Opens a browser and plays the requested content on YouTube.

    Args:
        payload (dict): Intent entities containing the YouTube search query.
                        Expected format: {"query": "<search term>"}

    Returns:
        str: Status message indicating the playback action or failure.
    """
    logger.debug("Payload received: %s", payload)

    fallback = "No content specified for YouTube playback"

    content = payload.get("query")
    
    # Query is required to play content on YouTube
    if not content:
        logger.warning("YouTube playback requested without query")
        return fallback
    
    try:
        logger.debug("YouTube playback initiation started | query=%s", content)

        # Open youtube in browser and play requested content
        pywhatkit.playonyt(content)

        result = f'Playing "{content}" on YouTube'
        logger.debug("YouTube playback initiated successfully | query=%s", content)
        return result
    
    except Exception:
        # Covers browser issues, network errors, or pywhatkit failures
        logger.exception("Failed to initiate YouTube playback")
        return "Unable to play the requested content on YouTube"


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()

    content = input("What do you want to play on YouTube: ")
    content_query = {"query": content}

    youtube_player(content_query)
