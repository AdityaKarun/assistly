from datetime import datetime

from modules.date_and_time import get_date_time

def greet():
    """
    Generates a greeting based on the current time of day.

    Args:
        None

    Returns:
        str: Greeting message appropriate for the current time.
    """
    current_time, _, _ = get_date_time()
    hour = datetime.strptime(current_time, "%I:%M %p").hour

    # Time-of-day based greeting selection
    if hour >= 5 and hour < 12:
        greeting = "Good Morning"
    elif  hour >= 12 and hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return greeting


if __name__ == "__main__":
    greeting = greet()
    print(f"{greeting}")
