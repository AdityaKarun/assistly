import logging
import os
import sys
import webbrowser

logger = logging.getLogger(__name__)

def open_app_or_url(payload):
    """
    Opens a desktop application or navigates to a URL based on intent payload.

    Args:
        payload (dict): Intent entities containing type and target details.

    Returns:
        str: Status message indicating the result of the operation.
    """
    logger.debug("Payload received: %s", payload)

    request_type = payload.get("type")
 
    if request_type == "app":
        exe = payload.get("executable")

        # Executable name is required to launch an application
        if not exe:
            logger.warning("App launch requested without executable")
            return "No executable provided"

        # App launching is supported only on Windows systems
        if not sys.platform.startswith("win"):
            logger.warning("App launch requested on unsupported platform | platform=%s", sys.platform)
            return "App launching is only supported on Windows"
            
        try:
            logger.debug("App launch initiation started | executable=%s", exe)
            os.startfile(exe)
            logger.debug("App launch initiated successfully | executable=%s", exe)
            return f"Opening {payload.get('name')}"

        except FileNotFoundError:
            logger.warning("Executable not found | executable=%s", exe)
            return f"Application '{exe}' is not installed or not found"
        
        except OSError:
            logger.exception("Failed to initiate app launch")
            return "Failed to launch application"

    elif request_type == "url":
        target_url = payload.get("url")

        # URL must be present for navigation requests
        if not target_url:
            logger.warning("URL navigation requested without URL")
            return "No URL provided"
        
        try:
            logger.debug("URL navigation initiation started | url=%s", target_url)
            webbrowser.open(target_url)
            logger.debug("URL navigation initiated successfully | url=%s", target_url)
            return f"Navigating to {payload.get('name')}"
        
        except Exception:
            logger.exception("Failed to initiate URL navigation")
            return "Failed to open the requested URL"

    else:
        logger.warning("Invalid open_app_or_url request type | type=%s", request_type)
        return "Invalid Request"


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()

    request_type = input("Enter request type (app or url): ")
    request_resource = input("Enter resource (app executable or url): ")

    if request_type == "app":
        payload = {"type": request_type, "name": "app_name", "executable": request_resource}

    elif request_type == "url":
        payload = {"type": request_type, "name": "url_name", "url": request_resource}

    open_app_or_url(payload)
