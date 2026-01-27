from datetime import datetime

def get_date_time(payload):
    """
    Generates a human-readable response for requested date/time information.

    Args:
        payload (dict): Contains an "info_type" key with a list of requested items
                        such as ["time", "date", "day"].

    Returns:
        str: A formatted sentence describing the requested date/time details.
    """

    # Default to all supported values if nothing specific is requested
    requested_info = payload.get("info_type", ["time", "date", "day"])

    now = datetime.now()

    info_map = {
        "time": now.strftime("%I:%M %p"), # "10:30 PM"
        "date": now.strftime("%B %d, %Y"), # "November 6, 2025"
        "day": now.strftime("%A") # "Thursday"
    }

    response = []

    # Build response fragments in the order requested by the user
    for info in requested_info:
        if info in info_map:
            value = info_map[info]

            if info == "time":
                response.append(f"The current time is {value}")
            
            elif info == "date":
                response.append(f"Today's date is {value}")

            elif info == "day":
                response.append(f"The day is {value}")

    # Handle cases where no valid request types were provided
    if len(response) == 0:
        return "I couldn't determine what date/time information you need."
    
    # Join fragments into a grammatically correct sentence
    elif len(response) == 1:
        return response[0] + "."
    
    elif len(response) == 2:
        return response[0] + " and " + response[1] + "."
    
    else:
        return response[0] + ", " + response[1] + " and " + response[2] + "."


if __name__ == "__main__":
    no_of_items = int(input("Enter the number of items to be requested: "))
    requested_info = []

    for i in range(no_of_items):
        info = input("Enter what you want to request (time or date or day): ")
        requested_info.append(info)

    payload = {"info_type": requested_info}
    response = get_date_time(payload)
    print(response)
