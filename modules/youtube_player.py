import pywhatkit

def youtube_player(content):
    """
    Opens a browser and plays the requested content on YouTube.

    Args:
        payload (dict): Intent entities containing the YouTube search query.

    Returns:
        str: Status message indicating the playback action.
    """
    content_query = content.get("query")
    
    # Query is required to play content on YouTube
    if not content_query:
        return "No content specified for YouTube playback."
    
    pywhatkit.playonyt(content)
    return f"Playing \"{content_query}\" on YouTube"

if __name__ == "__main__":
    content = input("What do you want to play on YouTube: ")
    content_query = {"query": content}
    youtube_player(content_query)
