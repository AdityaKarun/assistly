import logging
import time
import sys
import psutil

logger = logging.getLogger(__name__)

def get_battery_status():
    """
    Retrieves current battery percentage and charging status.

    Args:
        None

    Returns:
        str: Human-readable battery status message or error message on failure.
    """
    try:
        battery = psutil.sensors_battery()
    except Exception:
        logger.exception("Failed to access battery information")
        return "Could not access battery information"
    
    # Some systems do not expose battery data
    if battery is None:
        logger.warning("Battery information unavailable on this system")
        return "Battery information is unavailable"
    
    percent = battery.percent
    plugged = battery.power_plugged

    if plugged:
        result = f"Battery is {percent}% and currently charging"
    else:
        result = f"Battery is {percent}%"
    
    logger.debug("Battery status generated | percent=%s plugged=%s", percent, plugged)
    return result
    
def get_cpu_usage():
    """
    Retrieves current CPU usage percentage.

    Args:
        None

    Returns:
        str: Human-readable CPU usage message or error message on failure.
    """
    try:
        usage = psutil.cpu_percent(interval=1)
    except Exception:
        logger.exception("Failed to retrieve CPU usage")
        return "Could not retrieve CPU usage"

    result = f"Current CPU usage is {usage}%"

    logger.debug("CPU usage generated | usage=%s", usage)
    return result

def get_ram_status():
    """
    Retrieves total and available system memory.

    Args:
        None

    Returns:
        str: Human-readable RAM usage message or error message on failure.
    """
    try:
        mem = psutil.virtual_memory()
    except Exception:
        logger.exception("Failed to retrieve memory information")
        return "Could not retrieve memory information"
    
    total = mem.total / (1024 ** 3)
    available = mem.available / (1024 ** 3)

    result = f"Out of {total:.1f} gigabytes, {available:.1f} gigabytes of RAM is currently free"

    logger.debug("RAM status generated | total_gb=%.1f available_gb=%.1f", total, available)
    return result

def get_disk_status():
    """
    Retrieves disk usage statistics for the primary drive.

    Args:
        None

    Returns:
        str: Human-readable disk usage message or error message on failure.
    """

    # Disk statistics are currently limited to Windows
    if not sys.platform.startswith("win"):
        logger.warning("Disk statistics requested on unsupported platform | platform=%s", sys.platform)
        return "Disk statistics is only supported on Windows"

    drive = "C:\\"

    try:
        usage = psutil.disk_usage(drive)
    except Exception:
        logger.exception("Failed to access disk information")
        return "Could not access disk information"
    
    total = usage.total / (1024 ** 3)
    available = usage.free / (1024 ** 3)

    result = f"Drive C has {available:.1f} GB of free space out of a total {total:.1f} GB"

    logger.debug("Disk status generated | drive=%s total_gb=%.1f free_gb=%.1f", drive, total, available)
    return result

def get_uptime():
    """
    Calculates how long the system has been running.

    Args:
        None

    Returns:
        str: Human-readable system uptime message or error message on failure.
    """
    try:
        boot_time = psutil.boot_time()
    except Exception:
        logger.exception("Failed to retrieve system uptime")
        return "Could not retrieve system uptime"
    
    uptime_seconds = int(time.time() - boot_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60

    if hours == 0:
        result = f"The system has been running for {minutes} minutes"
    else:
        result = f"The system has been running for {hours} hours and {minutes} minutes"

    logger.debug("Uptime generated | hours=%s minutes=%s", hours, minutes)
    return result

SYSTEM_INFO_HANDLERS = {
    "battery": get_battery_status,
    "cpu": get_cpu_usage,
    "memory": get_ram_status,
    "storage": get_disk_status,
    "uptime": get_uptime
}

def handle_system_info(payload):
    """
    Routes system information requests to the appropriate handler.

    Args:
        payload (dict): Intent entities containing the requested resource.

    Returns:
        str: Result returned by the matched system information handler or error message on failure.
    """
    logger.debug("Payload received: %s", payload)

    target_resource = payload.get("resource")

    # Resource key is required to determine handler
    if not target_resource:
        logger.warning("System info requested without resource")
        return "No resource was queried"
    
    target_resource = target_resource.strip().lower()
    handler = SYSTEM_INFO_HANDLERS.get(target_resource)

    # Unsupported resources are rejected explicitly
    if not handler:
        logger.warning("Unsupported system info requested | resource=%s", target_resource)
        return "This system information is not supported yet"
    
    logger.debug("System info handler selected | handler=%s", handler.__name__)
    result = handler()
    logger.debug("System info response generated | resource=%s", target_resource)
    return result


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()

    request_resource = input("Enter resource ('battery' or 'cpu' or 'memory' or 'storage' or 'uptime'): ")
    payload = {"resource": request_resource}
    handle_system_info(payload)
