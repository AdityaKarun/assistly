import pyjokes

def get_joke():
    """
    Retrieves a random programming-related joke.

    Args:
        None

    Returns:
        str: A randomly selected programming joke.
    """
    joke = pyjokes.get_joke(language="en")
    
    return joke


if __name__ == "__main__":
    joke = get_joke()
    print(joke)
