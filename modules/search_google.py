import pywhatkit

def search_google(payload):
    """
    Performs a Google search using the provided query.

    Args:
        payload (dict): Intent entities containing the search query.

    Returns:
        str: Status message indicating the search action.
    """
    search_query = payload.get("query")

    # Query is required to perform a search
    if not search_query:
        return "No search query provided."
    
    pywhatkit.search(search_query)
    return f"Searching \"{search_query}\" on Google"

if __name__ == "__main__":
    search_query = input("Search Google: ")
    payload = {"query": search_query}
    search_google(payload)
