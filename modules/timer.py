import logging
import time
import threading

logger = logging.getLogger(__name__)

# Hard limit of 1 hour to prevent very long timers
MAX_TIMER_SECONDS = 3600

def worker(seconds, speaker):
    """
    Waits for the specified duration and announces timer completion.

    Args:
        seconds (int): Number of seconds to wait before completion.
        speaker (object): Text-to-speech handler for announcing completion.

    Returns:
        None
    """
    try:
        logger.debug("Timer worker started | duration=%s seconds", seconds)
        time.sleep(seconds)
        speaker.speak("Timer finished")
        logger.debug("Timer worker completed | duration=%s seconds", seconds)

    except Exception:
        # Any unexpected failure during countdown or announcement
        logger.exception("Timer worker failed unexpectedly")

def run_timer(payload, speaker=None):
    """
    Validates timer input and starts a non-blocking countdown.

    Args:
        payload (dict): Intent entities containing timer duration.
        speaker (object | None): Text-to-speech handler for timer completion.

    Returns:
        str: Status message indicating timer state or error message on failure.
    """
    logger.debug("Payload received: %s", payload)

    if speaker is None:
        logger.warning("Timer requested without speaker instance")
        return "Speaker must be provided when running timer"
    
    try:
        timer_duration = int(payload.get("duration"))
    except (TypeError, ValueError):
        logger.warning("Invalid timer duration provided | payload=%s", payload)
        return "Invalid timer duration"
    
    if timer_duration <= 0:
        logger.warning("Non-positive timer duration requested | duration=%s", timer_duration)
        return "Invalid timer duration"
    
    if timer_duration > MAX_TIMER_SECONDS:
        logger.warning("Timer duration exceeds maximum limit | duration=%s max=%s",
            timer_duration,
            MAX_TIMER_SECONDS
        )
        return "Sorry, I can only set timers up to one hour"
    
    logger.debug("Timer initiation started | duration=%s seconds", timer_duration)

    # Create a daemon thread so the timer does not block program exit
    timer_thread = threading.Thread(
        target=worker, 
        args=(timer_duration, speaker), 
        daemon=True, 
        name="TimerThread"
    )

    # Start the timer asynchronously
    timer_thread.start()

    logger.debug("Timer initiated successfully | duration=%s seconds", timer_duration)
    return f"Timer started for {timer_duration} seconds"


if __name__ == "__main__":
    from core.logger_config import setup_logging
    from core.speech import Speech

    setup_logging()
    speaker = Speech()

    seconds = int(input("Enter the number of seconds for the timer: "))
    payload = {"duration": seconds}

    run_timer(payload, speaker)
    
    # Keep process alive long enough for timer completion in standalone mode
    time.sleep(seconds + 3)
