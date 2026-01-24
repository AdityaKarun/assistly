import random

# Predefined short acknowledgements for courtesy-style responses
RESPONSES = [
    "You're welcome.",
    "No problem.",
    "Anytime.",
    "All good."
]

def handle_courtesy():
    """
    Returns a short acknowledgement response.

    Args:
        None

    Returns:
        str: A randomly selected courtesy response.
    """
    return random.choice(RESPONSES)


if __name__ == "__main__":
    input("Hit Enter to get a courtesy response.")
    response = handle_courtesy()
    print(response)
