import time
import sys
import psutil

def get_battery_status():
    """
    Retrieves current battery percentage and charging status.

    Args:
        None

    Returns:
        str: Human-readable battery status message.
    """
    try:
        battery = psutil.sensors_battery()
    except Exception:
        return "I could not access battery information."
    
    # Some systems do not expose battery data
    if battery is None:
        return "Battery information is unavailable."
    
    percent = battery.percent
    plugged = battery.power_plugged

    if plugged:
        return f"Battery is {percent}% and currently charging."
    else:
        return f"Battery is {percent}%."
    
def get_cpu_usage():
    """
    Retrieves current CPU usage percentage.

    Args:
        None

    Returns:
        str: Human-readable CPU usage message.
    """
    try:
        usage = psutil.cpu_percent(interval=1)
    except Exception:
        return "I could not retrieve CPU usage."

    return f"Current CPU usage is {usage}%."

def get_ram_status():
    """
    Retrieves total and available system memory.

    Args:
        None

    Returns:
        str: Human-readable RAM usage message.
    """
    try:
        mem = psutil.virtual_memory()
    except Exception:
        return "I could not retrieve memory information."
    
    total = mem.total / (1024 ** 3)
    available = mem.available / (1024 ** 3)

    return f"Out of {total:.1f} gigabytes, {available:.1f} gigabytes of RAM is currently free."

def get_disk_status():
    """
    Retrieves disk usage statistics for the primary drive.

    Args:
        None

    Returns:
        str: Human-readable disk usage message.
    """

    # Disk statistics are currently limited to Windows
    if not sys.platform.startswith("win"):
            return "Disk statistics is only supported on Windows."

    drive="C:\\"

    try:
        usage = psutil.disk_usage(drive)
    except Exception:
        return "I could not access disk information."
    
    total = usage.total / (1024 ** 3)
    available = usage.free / (1024 ** 3)

    return f"Drive C has {available:.1f} GB of free space out of a total {total:.1f} GB."

def get_uptime():
    """
    Calculates how long the system has been running.

    Args:
        None

    Returns:
        str: Human-readable system uptime message.
    """
    try:
        boot_time = psutil.boot_time()
    except Exception:
        return "I could not retrieve system uptime."
    
    uptime_seconds = int(time.time() - boot_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60

    if hours == 0:
        return f"The system has been running for {minutes} minutes."

    return f"The system has been running for {hours} hours and {minutes} minutes."

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
        str: Result returned by the matched system information handler.
    """
    target_resource = payload.get("resource")

    # Resource key is required to determine handler
    if not target_resource:
        return "No resource was queried."
    
    target_resource = target_resource.strip().lower()
    handler = SYSTEM_INFO_HANDLERS.get(target_resource)

    # Unsupported resources are rejected explicitly
    if not handler:
        return "This system information is not supported yet."
    
    return handler()


if __name__ == "__main__":
    request_resource = input("Enter resource ('battery' or 'cpu' or 'memory' or 'storage' or 'uptime'): ")
    payload = {"resource": request_resource}
    response = handle_system_info(payload)
    print(response)
