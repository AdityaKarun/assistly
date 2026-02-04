import logging
import pyjokes

logger = logging.getLogger(__name__)

def get_joke():
    """
    Retrieves a random programming-related joke.

    Args:
        None

    Returns:
        str: A randomly selected programming joke.
    """
    joke = pyjokes.get_joke(language="en")
    logger.debug("Programming joke generated successfully: %s", joke)

    return joke


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()
    get_joke()
