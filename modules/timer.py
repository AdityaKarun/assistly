import time
import threading

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
    time.sleep(seconds)
    speaker.speak("Timer finished.")

def run_timer(payload, speaker=None):
    """
    Validates timer input and starts a non-blocking countdown.

    Args:
        payload (dict): Intent entities containing timer duration.
        speaker (object | None): Text-to-speech handler for timer completion.

    Returns:
        str: Status message indicating timer state or validation error.
    """
    if speaker is None:
        return "Speaker must be provided when running timer."
    
    try:
        timer_duration = int(payload.get("duration"))
    except (TypeError, ValueError):
        return "Invalid timer duration."
    
    if timer_duration <= 0:
        return "Invalid timer duration."
    
    if timer_duration > MAX_TIMER_SECONDS:
        return "Sorry, I can only set timers up to one hour."
    
    # Create a daemon thread so the timer does not block program exit
    timer_thread = threading.Thread(
        target=worker, 
        args=(timer_duration, speaker), 
        daemon=True, 
        name="TimerThread"
    )

    # Start the timer asynchronously
    timer_thread.start()

    return f"Timer started for {timer_duration} seconds"


if __name__ == "__main__":
    from core.speech import Speech

    speaker = Speech()
    seconds = int(input("Enter the number of seconds for the timer: "))
    payload = {"duration": seconds}

    response = run_timer(payload, speaker)
    print(response)
    
    # Keep process alive long enough for timer completion in standalone mode
    time.sleep(seconds+2)
