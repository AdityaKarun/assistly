from datetime import datetime

def get_date_time():
    """
    Retrieves the current time, date, and day of the week.

    Args:
        None

    Returns:
        tuple: (current_time, date, day) as formatted strings.
    """
    now = datetime.now()

    # Get current time in 12-hour format (e.g., "10:30 PM")
    current_time = now.strftime("%I:%M %p")

    # Get current date in full format (e.g., "November 6, 2025")
    date = now.strftime("%B %d, %Y")

    # Get current day of the week (e.g., "Thursday")
    day = now.strftime("%A")

    return current_time, date, day


if __name__ == "__main__":
    current_time, date, day = get_date_time()
    print(f"Current Time: {current_time}")
    print(f"Date: {date}")
    print(f"Day: {day}")
