import logging

from core.recognizer import Recognizer
from core.speech import Speech
from core.intent_classifier import IntentEngine
from core.router import Router
from core.logger_config import setup_logging

from modules.greet import greet

logger = logging.getLogger(__name__)

def main():
    logger.info("Assistly started")
    greeting = greet()

    recognizer = Recognizer()
    speaker = Speech()
    intent = IntentEngine()
    route = Router(speaker)

    speaker.speak(greeting)

    while True:
        command = recognizer.recognize_command()

        # Skip processing if speech recognition failed
        if not command:
            continue

        intent_result = intent.classify(command)
        response = route.define_route(intent_result)

        speaker.speak(response)

        # Exit loop when explicit termination intent is returned
        if response == "Goodbye":
            break
    
    logger.info("Assistly stopped")


if __name__ == "__main__":
    setup_logging()
    main()