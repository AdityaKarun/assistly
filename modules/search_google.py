import logging
import pywhatkit

logger = logging.getLogger(__name__)

def search_google(payload):
    """
    Performs a Google search using the provided query.

    Args:
        payload (dict): Intent entities containing the Google search query.
                        Expected format: {"query": "<search term>"}

    Returns:
        str: Status message indicating the search action or failure.
    """
    logger.debug("Payload received: %s", payload)

    fallback = "No query specified for Google search"

    search_term = payload.get("query")

    # Query is required to search on Google
    if not search_term:
        logger.warning("Google search requested without query")
        return fallback
    
    try:
        logger.debug("Google search initiation started | query=%s", search_term)

        # Open google.com in browser and search requested term
        pywhatkit.search(search_term)

        result = f'Searching "{search_term}" on Google'
        logger.debug("Google search initiated successfully | query=%s", search_term)
        return result
    
    except Exception:
        # Covers browser issues, network errors, or pywhatkit failures
        logger.exception("Failed to initiate Google search")
        return "Unable to search the requested term on Google"


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()

    search_query = input("Search Google: ")
    payload = {"query": search_query}

    search_google(payload)
