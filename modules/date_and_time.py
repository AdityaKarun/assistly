import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_date_time(payload):
    """
    Generates a human-readable response for requested date/time information.

    Args:
        payload (dict): Contains an "info_type" key with a list of requested items
                        such as ["time", "date", "day"].

    Returns:
        str: A formatted sentence describing the requested date/time details,
             or a fallback message if the request is invalid.
    """

    logger.debug("Payload received: %s", payload)

    # Extract requested info types, defaulting later if empty or missing    
    requested_info = payload.get("info_type", ["time", "date", "day"])
    logger.debug("Requested information: %s", requested_info)

    if not requested_info:
        requested_info = ["time", "date", "day"]
        logger.warning("Requested information list empty, falling back to default %s", requested_info)

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

        else:
            logger.warning("Unknown info_type requested: %s", info)

    logger.debug("Built response list: %s", response)

    # Handle cases where no valid request types were provided
    if len(response) == 0:
        result = "I couldn't determine what date/time information you need."
        logger.warning("Unable to process date/time information")
        return result
    
    # Join fragments into a grammatically correct sentence
    elif len(response) == 1:
        result = response[0] + "."
    
    elif len(response) == 2:
        result = response[0] + " and " + response[1] + "."
    
    else:
        result = response[0] + ", " + response[1] + " and " + response[2] + "."

    logger.debug("Generated date/time response successfully | %s", result)
    return result


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()

    no_of_items = int(input("Enter the number of items to be requested: "))
    requested_info = []

    for i in range(no_of_items):
        info = input("Enter what you want to request (time or date or day): ")
        requested_info.append(info)

    payload = {"info_type": requested_info}
    get_date_time(payload)
