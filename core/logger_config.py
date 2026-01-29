import os
import logging

# Directory and file path for application logs
LOG_DIR = os.path.join("logs")
LOG_FILE = os.path.join(LOG_DIR, "assistly.log")

def setup_logging():
    """
    Configures application-wide logging with file and console handlers.

    Args:
        None

    Returns:
        None
    """
    
    # Ensure log directory exists before creating file handlers
    os.makedirs(LOG_DIR, exist_ok=True)

    # Get the root logger to configure
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Remove existing handlers to prevent duplicate logs
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    # File handler (DEBUG and above)
    file_handler = logging.FileHandler(filename=LOG_FILE, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(file_formatter)

    # Console handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)

    # Attach handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Silence noisy third-party libraries
    logging.getLogger("comtypes").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    root_logger.debug("Logging initialized")
