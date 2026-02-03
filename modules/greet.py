import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def greet():
    """
    Generates a greeting based on the current time of day.

    Args:
        None

    Returns:
        str: Greeting message appropriate for the current time.
    """
    hour = hour = datetime.now().hour

    # Time-of-day based greeting selection
    if hour >= 5 and hour < 12:
        greeting = "Good Morning"
    elif  hour >= 12 and hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    logger.debug("Greetings generated successfully: %s", greeting)
    return greeting


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()
    greet()
