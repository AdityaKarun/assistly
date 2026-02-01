import logging
import random

logger = logging.getLogger(__name__)

# Predefined short acknowledgements for courtesy-style responses
RESPONSES = [
    "You're welcome.",
    "No problem.",
    "Anytime."
]

def handle_courtesy():
    """
    Returns a short acknowledgement response.

    Args:
        None

    Returns:
        str: A randomly selected courtesy response.
    """
    response = random.choice(RESPONSES)
    logger.debug("Courtesy response generated successfully: %s", response)
    return response


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()
    handle_courtesy()
