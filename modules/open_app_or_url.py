import os
import sys
import webbrowser

def open_app_or_url(payload):
    """
    Opens a desktop application or navigates to a URL based on intent payload.

    Args:
        payload (dict): Intent entities containing type and target details.

    Returns:
        str: Status message indicating the result of the operation.
    """
    request_type = payload.get("type")
 
    if request_type == "app":
        exe = payload.get("executable")

        # Executable name is required to launch an application
        if not exe:
            return "No executable provided."

        # App launching is supported only on Windows systems
        if not sys.platform.startswith("win"):
            return "App launching is only supported on Windows."
            
        try:
            os.startfile(exe)
            return f"Opening {payload.get('name')}."

        except FileNotFoundError:
            return f"Application '{exe}' is not installed or not found."
        
        except OSError:
            return f"Failed to open application."

    elif request_type == "url":
        target_url = payload.get("url")

        # URL must be present for navigation requests
        if not target_url:
            return "No URL provided."
        
        webbrowser.open(target_url)
        return f"Navigating to {payload.get('name')}."
    
    else:
        return "Invalid Request."


if __name__ == "__main__":
    request_type = input("Enter request type (app or url): ")
    request_resource = input("Enter resource (app executable or url): ")

    if request_type == "app":
        payload = {"type": request_type, "name": "app_name", "executable": request_resource}

    elif request_type == "url":
        payload = {"type": request_type, "name": "url_name", "url": request_resource}

    response = open_app_or_url(payload)
    print(response)
